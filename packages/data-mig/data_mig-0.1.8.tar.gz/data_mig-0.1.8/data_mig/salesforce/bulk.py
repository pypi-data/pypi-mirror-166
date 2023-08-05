from data_mig.utils.config import Config
from simple_salesforce.bulk import SFBulkType, SFBulkHandler
from simple_salesforce.util import call_salesforce
from data_mig.utils.exceptions import BatchFailureException
import simplejson as json
from collections import OrderedDict
import pandas as pd
import progressbar
from string import Template
from datetime import datetime, date,  timedelta
from time import sleep

class CustomBulkHandler(SFBulkHandler):
    def __getattr__(self, name):
        return CustomSFBulkType(object_name=name, bulk_url=self.bulk_url,
                          headers=self.headers, session=self.session)


class CustomSFBulkType(SFBulkType):
    # Override standard batch results to inject custom exceptions for invalid batch states
    active_job_id = None
    progress_bar = None
    data_size = None
    timezone_offset = None

    def _get_batch_results(self, job_id, batch_id, operation):
        """ retrieve a set of results from a completed job """

        url = "{}{}{}{}{}{}".format(self.bulk_url, 'job/', job_id, '/batch/',
                                    batch_id, '/result')

        result = call_salesforce(url=url, method='GET', session=self.session,
                                 headers=self.headers)

        batch = self._get_batch(job_id=job_id,
                                    batch_id=batch_id)

        self.active_job_id = job_id

        batch_status = batch['state']
        self._update_progress_bar()

        if operation in ('query', 'queryAll'):
            if batch_status in ['Failed']:
                raise BatchFailureException('ERROR: {stateMessage}'.format(**batch))

            if batch_status in ['InvalidBatch']:
                raise BatchFailureException('ERROR in query -- check read.yml job? Batch state: {}'.format(batch.get('stateMessage')))

            for batch_result in result.json():
                url_query_results = "{}{}{}".format(url, '/', batch_result)
                batch_query_result = call_salesforce(url=url_query_results,
                                                     method='GET',
                                                     session=self.session,
                                                     headers=self.headers
                                                     ).json()
                yield batch_query_result
        else:
            result = result.json()

            if batch_status in ['Failed', 'NotProcessed']:
                url = "{}{}{}{}{}{}".format(self.bulk_url, 'job/', job_id, '/batch/',
                                            batch_id, '/request')
                request = call_salesforce(url=url, method='GET', session=self.session,
                                          headers=self.headers).json()
                if len(request) > len(result):
                    diff = len(request) - len(result)
                    result.extend(
                        [{'success': False, 'created': False, 'id': None,
                          'errors': [{"statusCode": "BATCH BAILED",
                                      "message": "BATCH PROCESSING STOPPED BEFORE RECORD REACHED", "fields": []}]}]
                        * diff )
            yield result

    def _print_batch_status(self, status):
        print("""--------- Batch Stats (Batch Id: {id}\tJob Id: {jobId}) ---------
State: {state}\tMessage: {stateMessage}\t
Records Failed: {numberRecordsFailed}\tRecords Processed: {numberRecordsProcessed}
Time: {totalProcessingTime}\tAPI Time: {apiActiveProcessingTime}\tAPEX Time: {apexProcessingTime}
""".format(**status))

    def _update_progress_bar(self):
        status = self._get_job(self.active_job_id)
        state = status.get('state')
        batches_queued_or_in_progress = status.get('numberBatchesInProgress') + status.get('numberBatchesQueued')
        batches_total = status.get('numberBatchesTotal')
        batch_completed = state == 'Closed' and batches_queued_or_in_progress == 0
        number_records_processed = status.get('numberRecordsProcessed')
        number_records_failed = status.get('numberRecordsFailed')
        operation = status.get('operation')
        prefix = Template("${operation} ").substitute(**status)
        if not self.progress_bar and operation not in ['query', 'queryAll']:
            markers = [
                '\x1b[32m█\x1b[39m',  # Succeeded
                '\x1b[31m.\x1b[39m',  # Failed
                '\x1b[33m#\x1b[39m'  # In Progress
            ]
            widgets = [prefix, progressbar.SimpleProgress(), ' ', progressbar.Percentage(),
                       progressbar.MultiRangeBar("counts", markers=markers), ' ', progressbar.Timer(), ' ',
                       progressbar.AdaptiveETA()]
            self.progress_bar = progressbar.ProgressBar(widgets=widgets, max_value=self.data_size, redirect_stdout=True)
        # if not self.progress_bar and operation in ['query', 'queryAll']:
        #    self.progress_bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength, redirect_stdout=True)
        if self.progress_bar:
            self.progress_bar.update(number_records_processed, counts=[number_records_processed-number_records_failed,
                                                                       number_records_failed,
                                                                       self.data_size - number_records_processed])
            if state == 'Aborted':
                self.progress_bar.finish(end='\n\n')
                sleep(0.5)
                self._print_job_status_final(status)
            if not self.progress_bar.end_time and batch_completed:
                self.progress_bar.finish(end='\n\n')
                sleep(0.5)
                self._print_job_status_final(status)

    def _get_and_print_job_status(self, jobId):
        status = self._get_job(jobId)
        self._print_job_status(status)

    def _print_job_status(self, status):
        print("""--------- Job Status (Id: {id}) ---------
Operation:\t\t{operation}\tObject: {object}
Batches:\t\tIn Progress: {numberBatchesInProgress}\tQueued: {numberBatchesQueued}\tCompleted: {numberBatchesCompleted}\tFailed: {numberBatchesFailed}\tTotal: {numberBatchesTotal} 
Records:\t\tProcessed: {numberRecordsProcessed}\tFailed: {numberRecordsFailed}\tRetries: {numberRetries}
""".format(**status))

    def _print_job_status_final(self, status):
            print("""--------- Job Results (Id: {id}) ---------
    Operation:\t\t{operation}\tObject: {object}
    Batches:\t\tCompleted: {numberBatchesCompleted}\tFailed: {numberBatchesFailed}\tTotal: {numberBatchesTotal} 
    Records:\t\tProcessed: {numberRecordsProcessed}\tFailed: {numberRecordsFailed}\tRetries: {numberRetries}
    """.format(**status))

    def _create_job(self, operation, use_serial,
                    external_id_field=None):
        """ Create a bulk job

        Arguments:

        * operation -- Bulk operation to be performed by job
        * object_name -- SF object
        * use_serial -- Process batches in order
        * external_id_field -- unique identifier field for upsert operations
        """

        # Override content type
        if self.object_name in ['Attachment', 'ContentVersion']:
            content_type = 'ZIP_JSON'
        else:
            content_type = 'JSON'
        if use_serial:
            use_serial = 1
        else:
            use_serial = 0
        payload = {
            'operation': operation,
            'object': self.object_name,
            'concurrencyMode': use_serial,
            'contentType': 'JSON'
        }

        if operation == 'upsert':
            payload['externalIdFieldName'] = external_id_field

        url = "{}{}".format(self.bulk_url, 'job')

        result = call_salesforce(url=url, method='POST', session=self.session,
                                 headers=self.headers,
                                 data=json.dumps(payload))

        self.active_job_id = result.json().get('id')
        self.timezone_offset = self.timezone_offset or Config().SALESFORCE_CONFIG.get('timezone_offset', 0) or 0
        self._update_progress_bar()

        return result.json(object_pairs_hook=OrderedDict)

    def _close_job(self, job_id):
        super(CustomSFBulkType, self)._close_job(job_id)
        self._update_progress_bar()

    def _get_batch(self, job_id, batch_id):
        self._update_progress_bar()
        return super(CustomSFBulkType, self)._get_batch(job_id, batch_id)

    def _add_batch(self, job_id, data, operation):
        """ Add a set of data as a batch to an existing job
        Separating this out in case of later
        implementations involving multiple batches
        """

        url = "{}{}{}{}".format(self.bulk_url, 'job/', job_id, '/batch')
        headers = self.headers.copy()

        if operation not in ('query', 'queryAll'):
            try:
                data = json.dumps(data, allow_nan=False, ignore_nan=True, cls=SalesforceEncoder,
                                  timezone_offset=self.timezone_offset)
            except UnicodeDecodeError:
                # Attachment/Content Data
                headers['Content-Type'] = 'zip/json'

            self._update_progress_bar()

        result = call_salesforce(url=url, method='POST', session=self.session,
                                 headers=self.headers, data=data)
        return result.json(object_pairs_hook=OrderedDict)

    def get_batch_results(self, job_id, batch_id, operation):
        self._update_progress_bar()
        return self._get_batch_results(job_id, batch_id, operation)


class SalesforceEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        self.timezone_offset = kwargs.pop('timezone_offset') if 'timezone_offset' in kwargs else 0
        super(SalesforceEncoder, self).__init__(*args, **kwargs)

    def default(self, obj):
        if type(obj) in [type(pd.NaT)]:
            return None

        # https://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.Timestamp.html
        if type(obj) in [date]:
            return obj.isoformat()

        if type(obj) in [pd.Timestamp, datetime]:
            return (obj + timedelta(hours=self.timezone_offset)).isoformat()

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
