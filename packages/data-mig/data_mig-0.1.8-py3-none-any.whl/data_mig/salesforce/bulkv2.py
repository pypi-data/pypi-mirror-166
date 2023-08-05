import copy
import requests
import json
import time
from enum import Enum
import pandas as pd
import progressbar
from string import Template
from io import StringIO
from datetime import datetime
from enum import Enum
from data_mig.sql.tools import SQLTools
from sqlalchemy import dialects as sqlalchemy_dialects

BULK2_API_ENDPOINT_TEMPLATE = '{}/services/data/v{}/jobs/ingest'
BULK2_API_HEADER_TEMPLATE = {'Content-Type': 'application/json; charset=UTF-8', 'Accept': 'application/json',
                             'Authorization': 'Bearer {}'}


class BulkApiV2ResultsType(Enum):
    SUCCESSFUL = 'successfulResults'
    FAILURE = 'failedResults'
    UNPROCESSED = 'unprocessedrecords'


class BulkApiV2(object):
    def __init__(self, cfg, load_parameters=None, data=None, filename=None, external_id_field_name=None,
                 size_hint=None, split_size=None):
        self._cfg = cfg
        self._sqltools = SQLTools(cfg)
        self.endpoint = self.__get_endpoint(cfg)
        self.object = load_parameters['sf_object']
        self.operation = load_parameters['operation']
        self.load_parameters = load_parameters
        self.token = cfg.SALESFORCE_CONFIG.get('access_token')
        self.external_id_field_name = load_parameters.get('id')
        self.filename = filename
        self.data = data
        self.split_size = split_size
        self.progress_bar = None
        self.job_id = None
        self.number_records_processed = 0
        self.number_records_failed = 0
        self.state = None
        if size_hint:
            self.data_size = size_hint
        elif data:
            self.data_size = len(data)
        else:
            self.data_size = None

    def _update_progress_bar(self):
        status = self.get_status(self.job_id)
        batch_completed = (status.get('state') == 'JobComplete')
        prefix = Template("${operation} ").substitute(**status)
        if not self.progress_bar and self.operation not in ['query', 'queryAll']:
            markers = [
                '\x1b[32m█\x1b[39m',  # Succeeded
                '\x1b[31m.\x1b[39m',  # Failed
                '\x1b[33m#\x1b[39m'  # In Progress
            ]
            widgets = [prefix, progressbar.SimpleProgress(), ' ', progressbar.Percentage(),
                       progressbar.MultiRangeBar("counts", markers=markers), ' ', progressbar.Timer(), ' ',
                       progressbar.AdaptiveETA()]
            self.progress_bar = progressbar.ProgressBar(widgets=widgets, max_value=self.data_size, redirect_stdout=True)
        if self.progress_bar:
            self.progress_bar.update(self.number_records_processed,
                                     counts=[self.number_records_processed - self.number_records_failed,
                                             self.number_records_failed,
                                             self.data_size - self.number_records_processed])
            if self.state in ['Aborted', 'Failed'] or (not self.progress_bar.end_time and batch_completed):
                self.progress_bar.finish(end='\n\n')
                time.sleep(0.5)

    def _print_job_status_final(self, status):
        print("""--------- Job Results (Id: {id}) ---------
    Operation:\t\t{operation}\tObject: {object}
    Records:\t\tProcessed: {numberRecordsProcessed}\tFailed: {numberRecordsFailed}\tRetries: {retries}
    """.format(**status))

    def __get_endpoint(self, cfg):
        api_version = cfg.SALESFORCE_CONFIG['sf_version']
        ep = self.endpoint = BULK2_API_ENDPOINT_TEMPLATE.format(cfg.SALESFORCE_CONFIG.get('instance_url'), api_version)
        return ep

    def __get_header(self, contentType=None):
        header = copy.copy(BULK2_API_HEADER_TEMPLATE)
        header['Authorization'] = header['Authorization'].format(self.token)
        if contentType:
            header['Content-Type'] = contentType
        return header

    def __create_job(self):
        req = BulkApiV2Request(self.object, self.operation,
                               external_id_field_name=self.external_id_field_name).to_json()
        r = requests.post(self.endpoint, json=req, headers=self.__get_header())
        try:
            response = r.json()
            self.job_id = response['id']
            self.state = response['state']
            print('JOB Created with Id: {}'.format(self.job_id))
        except (ValueError, AttributeError):
            print('Create Failed: {}'.format(r.text))
            self.job_id = None

    def __upload(self, filename=None, data=None, content_type='text/csv'):
        url = '{}/{}/batches'.format(self.endpoint, self.job_id)
        header = self.__get_header(content_type)

        if not (filename or data):
            raise Exception('Must provide either filename or data')

        if filename:
            file = open(filename, 'rb')
            data = file.read()
            self.data = len(data)

        response = requests.put(url, data=data, headers=header)
        return response.status_code

    def __close_batch(self):
        close_url = '{}/{}'.format(self.endpoint, self.job_id)
        close_body = {"state": "UploadComplete"}
        close_response = requests.patch(close_url, headers=self.__get_header(), json=close_body)

        try:
            close_data = json.loads(close_response.text)
            self.state = close_data['state']
        except:
            self.state = 'Failure: Could not parse errorMessage: {}'.format(close_response.text)

        return self.state

    def get_status(self, job_id=None):
        job_id = job_id if job_id else self.job_id
        status_url = '{}/{}/'.format(self.endpoint, job_id)
        status_response = requests.get(status_url, headers=self.__get_header())
        status = None
        try:
            status = status_response.json()
            state = status.get('state')
            error_message = status.get('errorMessage')
            self.state = state
            self.number_records_processed = status.get('numberRecordsProcessed')
            self.number_records_failed = status.get('numberRecordsFailed')
            if error_message:
                print('Error: {}'.format(error_message))
        except ValueError:
            self.state = None
            print('Error: {}'.format(status_response.text))

        return status

    def upload_batch(self):
        self.__create_job()
        self.__upload(filename=self.filename, data=self.data.encode("utf-8"))
        self.__close_batch()

        while self.state in ['', 'InProgress', 'UploadComplete']:
            time.sleep(10)
            self._update_progress_bar()

        self._print_job_status_final(self.get_status())

        if self.number_records_failed:
            self.summarize_failures()

        self.log_results()

    def get_ingest_results(self, results_type, outputfile=None, job=None):
        if not isinstance(results_type, BulkApiV2ResultsType):
            raise KeyError('Results Type Must Be BulkApiV2ResultsType')

        if job:
            job_id = job
        else:
            job_id = self.job_id

        results_path_url = results_type.value
        url = '{}/{}/{}/'.format(self.endpoint, job_id, results_path_url)
        response = requests.get(url, headers=self.__get_header())

        if outputfile:
            f = open(outputfile, 'w+')
            f.write(response.text)
            f.close()
        else:
            return response

    def summarize_failures(self, job=None):
        print(f'--------- Error Summary (Id: {self.job_id}) ---------')
        df = pd.read_csv(StringIO(self.get_ingest_results(BulkApiV2ResultsType.FAILURE, job=job).text))
        summary = df.groupby('sf__Error')['sf__Error'].count()
        print(summary)
        print('----------------------------------------------------------')

    def log_results(self):
        [self.log_results_by_type(x) for x in BulkApiV2ResultsType]

    def log_results_by_type(self, results_type):
        destination_table = self._cfg.DATABASE_CONFIG.get('LOG_TABLE')
        if destination_table:
            results_csv = StringIO(self.get_ingest_results(results_type).text)
            results_df = pd.read_csv(results_csv)
            results_df['request'] = results_df[[x for x in
                                                results_df.columns
                                                if not x.startswith('sf__')]].apply(lambda x: json.loads(x.to_json()),
                                                                                    axis=1).tolist()

            results_df = results_df[[x for x in results_df.columns if x.startswith('sf__') or x == 'request']]
            results_df.insert(0, 'timestamp', datetime.now())
            results_df.insert(1, 'series', self.load_parameters.get('series'))
            results_df.insert(2, 'job_number', self.load_parameters.get('level'))
            results_df.insert(3, 'object', self.object)
            results_df.insert(4, 'operation', self.operation)
            results_df.insert(5, 'job_id', self.job_id)
            results_df = results_df.rename(columns={'sf__Id': 'id', 'sf__Created': 'created', 'sf__Error': 'errors'})

            if 'id' not in results_df.columns:
                results_df.insert(6, 'id', None)

            if 'success' not in results_df.columns:
                results_df.insert(6, 'success', results_type == BulkApiV2ResultsType.SUCCESSFUL)

            if 'created' not in results_df.columns:
                results_df.insert(6, 'created', False)

            if 'errors' not in results_df.columns:
                results_df.insert(6, 'errors', None)

            results_df = results_df[['timestamp', 'series', 'job_number', 'object', 'operation', 'job_id', 'success',
                                     'created', 'id', 'errors', 'request']]

            results_df.to_sql(destination_table, self._sqltools.sqlalchemy_connect_to_db(), if_exists='append',
                              dtype={'request': sqlalchemy_dialects.mssql.JSON})


class BulkApiV2Request(object):
    class delimiters(Enum):
        BACKQUOTE = 'BACKQUOTE'
        CARET = 'CARET'
        COMMA = 'COMMA'
        PIPE = 'PIPE'
        TAB = 'TAB'

    class contentTypes(Enum):
        CSV = 'CSV'

    class operations(Enum):
        insert = 'insert'
        delete = 'delete'
        update = 'update'
        upsert = 'upsert'

    class lineEndings(Enum):
        LF = 'LF'
        CRLF = 'CRLF'

    __json_data = {}

    def __init__(self, sf_object, operation, external_id_field_name=None, line_ending=None):
        self.object = sf_object
        self.__json_data['externalIdFieldName'] = external_id_field_name
        self.__json_data['operation'] = operation
        self.__json_data['object'] = sf_object
        self.__json_data['columnDelimiter'] = self.delimiters.COMMA
        self.__json_data['lineEnding'] = line_ending if line_ending else self.lineEndings.LF
        self.__json_data['contentType'] = self.contentTypes.CSV

    def to_json(self):
        obj = self.__json_data
        json = {}
        for key in obj:
            if obj[key]:
                try:
                    json[key] = obj[key].value
                except:
                    json[key] = copy.copy(obj[key])

        return json
