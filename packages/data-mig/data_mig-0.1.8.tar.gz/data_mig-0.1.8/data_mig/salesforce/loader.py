from data_mig.sql.tools import *
from data_mig.salesforce.tools import *
from pprint import pprint
from data_mig.utils.exceptions import *
from datetime import datetime
from data_mig.salesforce.bulkv2 import BulkApiV2
from data_mig.salesforce.fileloader import SalesforceFileLoader
from data_mig.utils.logging import bcolors,Logging
import sqlalchemy
import pandas as pd
import json
import csv
import time


class SalesforceDataLoader(object):
    DEFAULT_BATCH_SIZE = 10000
    BOOLEAN_TRUE_VALUES = ['1', 'TRUE', 'FALSE', 'X', 'Y']
    AUDIT_FIELDS = ['CreatedDate', 'CreatedById', 'LastModifiedDate', 'LastModifiedById']
    AUDIT_FIELDS_UPPER = [c.upper() for c in AUDIT_FIELDS]

    def __init__(self, config):
        self._config = config
        self._st = SQLTools(config)
        self._sf_tools = SalesforceTools(config)
        self._logger = Logging(config).log
        self._sf_api = self._sf_tools.connect()

    def load_view(self, load_parameters):
        query = load_parameters.get('query')
        sf_object = load_parameters.get('sf_object')
        file = load_parameters.get('file_path') or load_parameters.get('file_data')
        if file:
            SalesforceFileLoader(self._config, load_parameters).load()
        else:
            df = self._st.query_to_dataframe(query)
            if df.isnull().all(axis=None):
                print('Nothing to load. Skipping.')
                return
            else:
                self._logger(f"Retrieved {len(df)} records...", type=LogEntryTypes.INFO)
            load_or_validate = 'Validation' if load_parameters.get('validate_only') else 'Load'
            print(('Starting {} to Salesforce ' + bcolors.OKGREEN + '{}' + bcolors.ENDC+'...').format(load_or_validate, sf_object, query))
            return self._load_dataframe(df, load_parameters)

    def _wait_for_batch(self, job_id, batch_id, timeout=60 * 10,
                       sleep_interval=10, statistics=False):
        waited = 0
        bulk = self._sf_tools.bulk
        while not bulk.is_batch_done(batch_id, job_id) and waited < timeout:
            if statistics:
                self._print_job_stats(job_id)
            time.sleep(sleep_interval)
            waited += sleep_interval

    def _load_chunked(self, data, load_parameters, columns):
        batch_size = load_parameters.get('batch_size') or self.DEFAULT_BATCH_SIZE
        use_serial = load_parameters.get('concurrency') == 'Serial'
        ext_id = load_parameters.get('id')
        sf_object = load_parameters.get('sf_object')
        operation = load_parameters.get('operation')
        bulk = self._sf_tools.bulk_api(sf_object)
        bulk.data_size = len(data)
        bulk.timezone_offset = load_parameters.get('timezone_offset')

        invalid_columns_in_data = self._get_invalid_sf_fields_from_column_list(sf_object, columns)
        if invalid_columns_in_data:
            print(Template('${start}Dropping invalid columns: ${columns}${end}').substitute(start=bcolors.WARNING,
                                                                                            columns=invalid_columns_in_data,
                                                                                            end=bcolors.ENDC))
            data_for_sf = [{k: v for k, v in d.items() if k not in invalid_columns_in_data} for d in data]
        else:
            data_for_sf = data

        results = bulk._bulk_operation(operation, data_for_sf, batch_size=batch_size, external_id_field=ext_id,
                                       use_serial=use_serial)
        results_list_of_list = False
        errors = []
        for record in results:
            # sometimes the results are a list of lists and sometimes they aren't.
            try:
                if not record.get('success'):
                    errors.extend(record.get('errors'))
            except AttributeError as error:
                for r in record:
                    if not r.get('success'):
                        errors.extend(r.get('errors'))
                results_list_of_list = True

        if results_list_of_list:
            results = [i for res in results for i in res]

        return {
            "results": self._log_results(data, results, load_parameters, jobid=bulk.active_job_id),
             "errors": errors
        }

    def _log_results(self, data, results, parameters, jobid=None):
        destination_table = self._config.DATABASE_CONFIG.get('LOG_TABLE')
        if destination_table:
            result_df = pd.DataFrame.from_records(results)
            request = pd.DataFrame(data)
            result_df['request'] = request.apply(lambda x: json.loads(x.to_json()), axis=1).tolist()
            result_df.insert(0, 'timestamp', datetime.now())
            result_df.insert(1, 'series', parameters.get('series'))
            result_df.insert(2, 'job_number', parameters.get('level'))
            result_df.insert(3, 'object', parameters.get('sf_object'))
            result_df.insert(4, 'operation', parameters.get('operation'))
            result_df.insert(5, 'job_id', jobid)
            result_df.to_sql(destination_table, self._st.sqlalchemy_connect_to_db(), if_exists='append',
                             dtype={'errors': sqlalchemy.dialects.mssql.JSON,
                                    'request': sqlalchemy.dialects.mssql.JSON})
            return result_df

    def dict2json(dictionary):
        return json.dumps(dictionary, ensure_ascii=False)

    def _load_dataframe(self, dataframe, load_parameters):
        sf_object = load_parameters.get('sf_object')
        batch_size = load_parameters.get('batch_size')
        ignore_schema_check = load_parameters.get('ignore_schema_check', False)
        ignore_invalid_fields = load_parameters.get('ignore_invalid_fields', False)
        filter_invalid = load_parameters.get('filter_invalid', False)
        operation = load_parameters.get('operation', '') if load_parameters.get('operation') else 'insert'
        audit_keys = load_parameters.get('insert_only_fields')
        if audit_keys:
            audit_keys = audit_keys.split(',') + self.AUDIT_FIELDS
        else:
            audit_keys = self.AUDIT_FIELDS

        try:
            self.check_schema(dataframe, sf_object, load_parameters)
        except ValidationException as e:
            if load_parameters.get('operation') in ['update', 'delete', 'hardDelete'] or ignore_schema_check:
                print('Bypassing required field validation for {}'.format(load_parameters.get('operation')))
                pass
            else:
                raise e

        if operation != 'insert' and load_parameters.get('drop_audit_on_upsert'):
            dataframe = self._remove_audit_columns(dataframe, audit_keys=audit_keys)

        # Filter 'nan' values from dictionary (from floats to_dict conversion)
        dataframe = dataframe.where(pd.notnull(dataframe), other=None)
        data = dataframe.to_dict('records')

        fields = [c.upper() for c in dataframe.columns]
        if operation != 'insert' and 'ID' in fields:
            self._remove_keys_when_id_present(data, keys=audit_keys)

        relationship_fields = [x for x in dataframe.columns if '.' in x]
        if relationship_fields:
            self._expand_relationship_fields(data, relationship_fields)

        id = load_parameters.get('id', 'Id')
        api_v2 = load_parameters.get('v2', False)

        if not load_parameters.get('validate_only'):
            if api_v2 and operation != 'query':
                # TODO: implement splitting to get around 100MB batch limit
                self._load_bulkv2(dataframe, load_parameters, ext_id=id, split_size=batch_size)
            else:
                return self._load_chunked(data, load_parameters, dataframe.columns)

    def _load_bulkv2(self, data, load_parameters, ext_id='Id', split_size=None):
        size_hint = len(data)
        data = data.to_csv(doublequote=True, quoting=csv.QUOTE_ALL, index=False, date_format='%Y-%m-%dZ')
        bulk = BulkApiV2(self._config, load_parameters=load_parameters, data=data,
                         external_id_field_name=ext_id, split_size=split_size, size_hint=size_hint)
        bulk.upload_batch()

    def _remove_keys_when_id_present(self, data, keys=AUDIT_FIELDS):
        audit_fields_upper = [c.upper() for c in keys]
        for rec in data:
            id_key = [c for c in rec.keys() if c.upper() == 'ID']
            if id_key:
                id_value = rec.get(id_key[0])
            else:
                continue
            if id_value:
                for field in list(rec):
                    if field.upper() in audit_fields_upper:
                        del rec[field]

    def _remove_audit_columns(self, df, audit_keys=None):
        if not audit_keys:
            audit_keys = self.AUDIT_FIELDS
        af_upper = [c.upper() for c in audit_keys]
        for c in df.columns:
            if c.upper() in af_upper:
                print('Dropping audit field {}'.format(c))
                df = df.drop(c, axis=1)
        return df

    def _expand_relationship_fields(self, data, relationship_fields):
        print('Expanding relationship fields: {}'.format(', '.join(relationship_fields)))
        for row in data:
            for field in relationship_fields:
                if row.get(field):
                    relationship = field.split('.')[0]
                    ext_id_field = field.split('.')[1]
                    row[relationship] = {ext_id_field: row[field]}
                try:
                    del row[field]
                except KeyError as E:
                    pass

    # TODO: filter out invalid dates
    def check_schema(self, df, sf_object, *args, **load_parameters):
        self._check_required_fields(df, sf_object)
        self._check_fields_against_schema(df, sf_object, raise_exception_on_invalid=(not load_parameters.get('ignore_invalid_fields')))
        if load_parameters.get('filter_invalid') and not load_parameters('validate_only'):
            self._filter_email_fields(df, sf_object)
            self._filter_boolean_fields(df, sf_object)
            self._filter_decimal_fields(df, sf_object)

    def _check_required_fields(self, df, sf_object):
        lowercase_df_columns = [l.lower() for l in df.columns]
        required_fields = self._sf_tools.get_required_fields(sf_object)

        missing_required_fields = [k for k, v in required_fields.items() if k.lower() not in lowercase_df_columns]

        if missing_required_fields:
            msg = 'Required field(s) ({}) not found.'.format(','.join(missing_required_fields))
            print(bcolors.FAIL + 'ERROR!!! {}'.format(msg) + bcolors.ENDC)
            raise ValidationException(msg)

    def _get_invalid_fields_against_schema(self, df, sf_object):
        return self._get_invalid_sf_fields_from_column_list(sf_object, df.columns)

    def _get_invalid_sf_fields_from_column_list(self, sf_object, columns):
        sf_field_metadata = self._sf_tools.get_object_fields(sf_object)
        lowercase_sf_columns = [k.lower() for k, v in sf_field_metadata.items()]
        unknown_fields = [k for k in columns if k.lower() not in lowercase_sf_columns]
        invalid_fields = []
        # check relationship fields, remove from invalid list if valid external ids
        for field in unknown_fields:
            try:
                if '.' in field:
                    relationship_name = field.split('.')[0]
                    field_from_relationship_name = \
                        [v for k, v in sf_field_metadata.items() if v.get('relationshipName')
                         and v.get('relationshipName').lower() == relationship_name.lower()][0]
                    sf_obj_rel = field_from_relationship_name['referenceTo'][0]
                    ext_id = field.split('.')[1]
                    relationship_md = self._sf_tools.get_object_fields(sf_obj_rel)
                    lowercase_ext_id_columns = [k.lower() for k, v in relationship_md.items() if v.get('idLookup')]
                    if ext_id.lower() not in lowercase_ext_id_columns:
                        invalid_fields.append(field)
                else:
                    invalid_fields.append(field)
            except Exception as e:
                print(Template('${start}Schema validation failed for field: ${field}: ${e}${end}').substitute(
                    start=bcolors.FAIL, field=field, e=e, end=bcolors.ENDC))
                pass
        return invalid_fields

    def _check_fields_against_schema(self, df, sf_object, raise_exception_on_invalid=True):
        invalid_fields = self._get_invalid_fields_against_schema(df, sf_object)
        try:
            if invalid_fields:
                raise ValidationException('Invalid column(s) found: ({})'.format(','.join(invalid_fields)))
        except ValidationException as e:
            if raise_exception_on_invalid:
                print('ERROR!!! {}'.format(e.message))
                raise ValidationException(e.message)
            else:
                print(Template('${start}${msg}${end}').substitute(start=bcolors.WARNING, msg = e.message,
                                                                  end=bcolors.ENDC))

    def _filter_email_fields(self, df, sf_object):
        sf_field_metadata = self._sf_tools.get_object_fields(sf_object)
        sf_email_fields = [k.lower() for k, v in sf_field_metadata.items() if v.get('type') == 'email']
        df_email_columns = [l for l in df.columns if l.lower() in sf_email_fields]
        if df_email_columns:
            print(Template('${start}${msg}${fields}${end}').substitute(start=bcolors.WARNING,
                                                                       msg='Filtering Email fields: ',
                                                                       fields=', '.join(df_email_columns),
                                                                       end=bcolors.ENDC))
            for field in df_email_columns:
                df[field] = df[field].apply(lambda x: x if x and self._is_valid_email(x) else None)

    def _filter_boolean_fields(self, df, sf_object):
        sf_field_metadata = self._sf_tools.get_object_fields(sf_object)
        sf_boolean_fields = [k.lower() for k, v in sf_field_metadata.items() if v.get('type') == 'boolean']
        df_boolean_columns = [l for l in df.columns if l.lower() in sf_boolean_fields]
        if df_boolean_columns:
            print(Template('${b}Standardizing Boolean fields: ${fields}${e}').substitute(
                b=bcolors.OKCYAN, fields=', '.join(df_boolean_columns), e=bcolors.ENDC))
            for field in df_boolean_columns:
                df[field] = df[field].apply(lambda x: True if str(x).upper() in self.BOOLEAN_TRUE_VALUES else False)
                df[field] = df[field].astype(bool)

    def _filter_decimal_fields(self, df, sf_object):
        sf_field_metadata = self._sf_tools.get_object_fields(sf_object)
        sf_numerical_fields = [k.lower() for k, v in sf_field_metadata.items() if v.get('type') in ['currency', 'percent', 'double', 'int']]
        df_decimal_columns = [k for k, v in df.dtypes.items() if v in ['float64', 'int64'] or k.lower() in sf_numerical_fields]
        if df_decimal_columns:
            print(Template('${b}Standardizing non-string fields: ${fields}${e}').substitute(
                b=bcolors.OKCYAN, fields=', '.join(df_decimal_columns), e=bcolors.ENDC))
            for field in df_decimal_columns:
                df[field] = df[field].apply(lambda x: x if x and ~pd.isnull(x) and x != 'nan' else None)
                df[field] = df[field].astype(float)

    def _divide_chunks(self, l, n=None):
        # looping till length l
        n = n or self.DEFAULT_BATCH_SIZE
        for i in range(0, len(l), n):
            yield l[i:i + n]

    # Salesforce KB: https://help.salesforce.com/articleView?id=000001145&language=en_US&type=1
    # using RE FROM https://gist.github.com/gregseth/5582254
    def _is_valid_email(self, email):
        re_filter = re.compile("""^(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$""", re.I)
        if len(email) > 7:
            if re_filter.match(email) != None:
                return True
            return False
        return False
