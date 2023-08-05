from string import Template
import requests
import sqlalchemy
from data_mig.sql.tools import SQLTools
from data_mig.salesforce.tools import SalesforceTools
from data_mig.salesforce.bulk import SalesforceEncoder
from datetime import datetime
import pandas as pd
import json
import progressbar


class SalesforceFileLoader(object):
    def __init__(self, config, job):
        self._config = config
        self._st = SQLTools(config)
        self._sf_tools = SalesforceTools(config)
        self._sf_api = self._sf_tools.connect()
        self._job = job
        self._sf_object = self._job.get('sf_object')
        self._query = self._job.get('query')
        self._file_path_column = self._job.get('file_path')
        self._file_data_column = self._job.get('file_data')
        self._log_table = self._config.DATABASE_CONFIG.get('LOG_TABLE')
        self._content_field = self._get_content_field()
        self._data = None
        self._data_count = None

    def load(self):
        data = self._sqlalchemy_query_db(self._query)
        count = self._sqlalchemy_query_db_counts(self._query)
        succeeded = 0
        failed = 0
        markers = [
            '\x1b[32m█\x1b[39m',  # Succeeded
            '\x1b[31m.\x1b[39m',  # Failed
            '\x1b[33m#\x1b[39m'  # In Progress
        ]

        widgets = [progressbar.SimpleProgress(), ' ', progressbar.Percentage(),
                   progressbar.MultiRangeBar("counts", markers=markers), ' ', progressbar.Timer(), ' ',
                   progressbar.AdaptiveETA()]
        bar = progressbar.ProgressBar(widgets=widgets, max_value=count, redirect_stdout=True)

        for request in data:
            request = dict(request)
            result = self._binary_multipart_upload(request)
            if result.ok:
                succeeded += 1
            else:
                failed += 1
            bar.update(succeeded+failed, counts=[succeeded, failed, count-succeeded-failed])
            self._log_entry_from_result(request, result)

        bar.finish(end='\n\n')

    def _encode_row_for_log(self, request):
        for k in request:
            v = request[k]
            if type(v) in [pd.Timestamp, datetime.date, datetime]:
                request[k] = v.isoformat()
            if type(v) in [bytes] or k in [self._file_data_column]:
                request[k] = None
        return request

    def _sqlalchemy_query_db(self, query):
        engine = self._st.sqlalchemy_connect_to_db(reset=True)
        return engine.execute(query)

    def _sqlalchemy_query_db_counts(self, query):

        engine = self._st.sqlalchemy_connect_to_db(reset=True)
        return engine.execute(self._st.result_count_query(query)).fetchone()[0]

    def _log_entry_from_result(self, request, response):
        rsp = response.json()
        if response.ok:
            cd_id = self._sf_tools.sf_api.__getattr__(self._sf_object).get(rsp.get('id')).get('ContentDocumentId')
            if cd_id:
                request['ContentDocumentId'] = cd_id
            result = {'timestamp': datetime.now(), 'series': self._job.get('series'),
                      'job_number': self._job.get('level'), 'object': self._job.get('sf_object'),
                      'operation': self._job.get('operation'), 'job_id': None, 'success': rsp.get('success'),
                      'created': rsp.get('success'), 'id': rsp.get('id'), 'errors': rsp.get('errors'),
                      'request': self._encode_row_for_log(request)}
        else:
            result = {'timestamp': datetime.now(), 'series': self._job.get('series'),
                      'job_number': self._job.get('level'), 'object': self._job.get('sf_object'),
                      'operation': self._job.get('operation'), 'job_id': None, 'success': False,
                      'created': False, 'id': None, 'errors': response.json(),
                      'request': self._encode_row_for_log(request)}

        if self._log_table:
            result_df = pd.DataFrame.from_records([result])
            result_df.to_sql(self._log_table, self._st.sqlalchemy_connect_to_db(), if_exists='append',
                             dtype={'errors': sqlalchemy.dialects.mssql.JSON,
                                    'request': sqlalchemy.dialects.mssql.JSON})

        return result

    def _get_content_field(self):
        sf_field_metadata = self._sf_tools.get_object_fields(self._sf_object)
        fields = [f for f, v in sf_field_metadata.items() if v.get('type') == 'base64']
        return fields[0]

    def _binary_multipart_upload(self, request):
        file_name = request[self._file_path_column]
        invalid_columns = self._get_invalid_fields(request.keys())

        if self._file_data_column:
            file_content = request[self._file_data_column]

        if not self._file_data_column:
            with open(file_name, mode='rb') as file:
                file_content = file.read()

        request = {key: val for (key, val) in request.items() if key not in invalid_columns
                   and key not in [self._file_data_column]}

        headers = {'Authorization': self._sf_tools.sf_api.headers.get('Authorization')}
        url = Template('${base}sobjects/${obj}/').substitute(base=self._sf_tools.sf_api.base_url, obj=self._sf_object)

        data = {
            "entity_content": ('', json.dumps(request, cls=SalesforceEncoder), 'application/json'),
            self._content_field: (file_name, file_content, "text/plain")
        }

        return requests.post(url, headers=headers, files=data)

    def _get_invalid_fields(self, columns):
        sf_field_metadata = self._sf_tools.get_object_fields(self._sf_object)
        lowercase_sf_columns = [c.lower() for c, v in sf_field_metadata.items()]
        return [c for c in columns if c.lower() not in lowercase_sf_columns]
