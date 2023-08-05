import pyodbc
from data_mig.salesforce.loader import SalesforceDataLoader
from data_mig.sql.loader import SQLDataLoader
from data_mig.sql.tools import SQLTools
from data_mig.salesforce.tools import SalesforceTools
from data_mig.utils.config import Config
from data_mig.utils.logging import Logging, LogEntryTypes
from data_mig.salesforce.oauth import SalesforceAuth
from data_mig.sql.loader import DEFAULT_SQL_CHUNK_SIZE
from simple_salesforce.exceptions import SalesforceResourceNotFound
from data_mig.utils.exceptions import DataMigException, BatchFailureException, RecordErrorException
from data_mig.utils.logging import bcolors
from data_mig import VERSION
from enum import Enum
from sqlalchemy.exc import ProgrammingError
import time
import sys


CURRENT_LEVEL_MIN = 1
CURRENT_LEVEL_MAX = 99999999
DEFAULT_READS_STANDARD_OBJECTS = ['Account', 'Contact', 'Opportunity', 'Lead', 'Campaign',
                                  'CampaignMember', 'CampaignMemberStatus', 'OpportunityContactRole']
DEFAULT_READS_NPSP_OBJECTS = ['npe01__OppPayment__c', 'npe03__Recurring_Donation__c',
                           'npe4__Relationship__c', 'npe5__Affiliation__c', 'npsp__Address__c',
                           'npsp__Allocation__c', 'npsp__Batch__c', 'npsp__General_Accounting_Unit__c',
                           'npsp__Grant_Deadline__c', 'npsp__Level__c', 'npsp__Partial_Soft_Credit__c']

DEFAULT_READS = DEFAULT_READS_STANDARD_OBJECTS
DEFAULT_READS_NPSP = list(DEFAULT_READS_NPSP_OBJECTS).append(DEFAULT_READS_STANDARD_OBJECTS)


class JobResult(Enum):
    COMPLETED = 'Completed'
    ERRORS = 'Completed With Errors'
    FAILED = 'Failed'


def yes_or_no(question):
    while "Invalid input":
        reply = str(input(question + ' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False


class Runner(object):

    def __init__(self, config):
        self._config = config
        self._logger = Logging(config)
        self._sf_loader = SalesforceDataLoader(config)
        self._sf_tools = SalesforceTools(config)
        self._sql_tools = SQLTools(config)

        self.userdata = self._sf_tools.sf_api._call_salesforce('GET',
                                self._sf_tools.sf_api.base_url + 'chatter/users/me').json()

        print(f'------------------{bcolors.OKCYAN}ARROYO v.{VERSION}{bcolors.ENDC}------------------')
        username = self.userdata.get('username')
        name = self.userdata.get('name')
        print(f'Salesforce User: {bcolors.OKGREEN}{name} ({username}){bcolors.ENDC}')
        print(f'Database: {bcolors.OKGREEN}{config.DATABASE_CONFIG.get("DATABASE")}{bcolors.ENDC}')

        self.org_edition = self._sf_tools.sf_api.query_all("""SELECT Id, OrganizationType
                FROM Organization""").get('records', [{"OrganizationType": None}])[0].get('OrganizationType')
        self.is_sandbox = self._sf_tools.sf_api.is_sandbox()
        self.is_production = not self.is_sandbox and self.org_edition != 'Developer Edition'
        self.is_email_enabled = self._sf_tools.is_email_enabled()
        self.dev_org = self.org_edition == 'Developer Edition'

        if self.is_production:
            print(f'Org Type: {bcolors.WARNING}WARNING: Production Org Connected ({self.org_edition}){bcolors.ENDC}')
        else:
            if self.is_sandbox:
                print(f'Org Type: {bcolors.OKGREEN}{self.org_edition} (Sandbox){bcolors.ENDC}')
            else:
                print(f'Org Type: {bcolors.OKGREEN}{self.org_edition}{bcolors.ENDC}')

        if not self.is_email_enabled:
            print(f'Email Deliverability: {bcolors.OKGREEN}Disabled{bcolors.ENDC}')

        # connect_confirm_type valid values = ['PROD', 'ALL', "EMAIL", "NONE"]
        confirm_type = config.SALESFORCE_CONFIG.get('connect_confirm_type', 'ALL')
        do_confirm = (confirm_type == 'PROD' and self.is_production) \
            or confirm_type == 'ALL' \
            or (confirm_type in ['EMAIL', 'PROD'] and self.is_email_enabled)
        if do_confirm:
            confirm_msg = f'{bcolors.WARNING}ALLOW LOAD OPERATIONS?{bcolors.ENDC}'
            if self.is_email_enabled:
                confirm_msg = f'{bcolors.FAIL}WARNING: EMAIL DELIVERABILITY IS ENABLED!!!{bcolors.ENDC} {confirm_msg}'
            if not yes_or_no(confirm_msg):
                self.load = None

                print(f'{bcolors.OKGREEN}LOAD OPERATIONS DISABLED{bcolors.ENDC}')
            else:
                print(f'{bcolors.WARNING}LOAD OPERATIONS ENABLED{bcolors.ENDC}')

    def reload_config(self):
        self._config.reload()

    def read_all(self, destination_table_prefix=None):
        try:
            self._sf_tools.get_object_fields('npe01__OppPayment__c')
            isNPSP = True
        except SalesforceResourceNotFound:
            isNPSP = False

        if self._config.reads:
            self.read_by_objects(self._config.reads.keys(), destination_table_prefix=destination_table_prefix)
        elif isNPSP:
            self.read_by_objects(DEFAULT_READS_NPSP, destination_table_prefix=destination_table_prefix)
        else:
            self.read_by_objects(DEFAULT_READS_STANDARD_OBJECTS, destination_table_prefix=destination_table_prefix)

    def read_by_objects(self, object_or_list_of_objects, destination_table_prefix=None):
        self._config.reload()
        if isinstance(object_or_list_of_objects, str):
            object_or_list_of_objects = [object_or_list_of_objects]

        filtered_loads = self._config.reads
        if filtered_loads:
            filtered_loads = {k: v for k, v in filtered_loads.items() if k in object_or_list_of_objects}

            for obj, read_operation in filtered_loads.items():
                if not read_operation.get('query'):
                    read_operation['query'] = self._generate_query_and_print_no_query_found_msg(obj)
                read_operation['label'] = read_operation.get('label', obj.title())
                self._read(read_operation, destination_table_prefix=destination_table_prefix)

        objects_not_in_read_yml = [x for x in object_or_list_of_objects if not filtered_loads or x not in self._config.reads.keys()]

        for obj in objects_not_in_read_yml:
            query = self._generate_query_and_print_no_query_found_msg(obj)
            read_operation = {**self._config.READ_DEFAULTS, 'label': obj, 'query': query}
            self.read = self._read(read_operation, destination_table_prefix=destination_table_prefix)

    def _generate_query_and_print_no_query_found_msg(self, obj):
        msg = "No read query found for {}. Generated query:".format(obj)
        print(msg)
        query = self.infer_sf_query(obj)
        print(bcolors.OKCYAN + query + bcolors.ENDC)
        return query

    def infer_sf_query(self, object):
        fields = self._sf_tools.get_object_fields(object)
        columns = [k for k, v in fields.items() if v.get('type') not in ['address', 'location', 'base64']]
        query = 'SELECT {} FROM {}'.format(', '.join(columns), object)
        return query

    def query_to_table(self, table, query='', object_name=None, query_all=False, if_exists='replace', method=None,
                       chunksize=None, indexes=None):
        if not table and (query or object_name):
            raise DataMigException('Either query or object must be along with table must be specified')

        if not query:
            query = self.infer_sf_query(object_name)
        else:
            query = query.replace('\n', ' ').replace('\r', ' ')

        label = object_name or SQLTools.get_table_from_query(query)

        read_operation = {'label': label, 'table': table, 'query':  query, 'indexes': indexes, 'query_all': query_all,
                          'if_exists': if_exists, 'method': method, 'chunksize': chunksize or DEFAULT_SQL_CHUNK_SIZE}
        self.read = self._read(read_operation)

    def _read(self, read_operation, try_count=1, destination_table_prefix=None):
        print(bcolors.OKGREEN + "Loading {} data from Salesforce".format(read_operation.get('label')) + bcolors.ENDC)
        try:
            read_args = {
                "destination_table": read_operation.get('table'),
                "indexes": read_operation.get('indexes'),
                "post_read_query": read_operation.get('post_read_query'),
                "query_all": read_operation.get('query_all'),
                "chunksize": read_operation.get('chunksize', DEFAULT_SQL_CHUNK_SIZE),
                "method": read_operation.get('method'),
                "if_exists": read_operation.get('if_exists'),
                "destination_table_prefix": destination_table_prefix
            }
            SQLDataLoader(self._config, read_operation.get('query'), **read_args).load()
        except Exception as e:
            print("Other Exception Caught")
            exc_type, value, traceback = sys.exc_info()
            self._logger.log('Exception: {} {}'.format(exc_type, value), type=LogEntryTypes.ERROR)
            self._logger.log(traceback, type=LogEntryTypes.ERROR)
            raise

    def open_sf_bulk_loads(self):
        self._sf_tools.open_sf_url('/lightning/setup/AsyncApiJobStatus/home')

    def _log_errors(self, errors, open_batch_screen=True):
        e_summary = self._summarize_errors(errors)
        e_count = sum(e_summary.values())
        e_summary = '\n'.join([f'{k} ({v})' for k,v in e_summary.items()])
        emsg = f"""Check batch at {self._config.SALESFORCE_CONFIG.get('instance_url')}/lightning/setup/AsyncApiJobStatus/home
{bcolors.BOLD}{e_count} Errors:
{e_summary}"""
        self._logger.log(emsg, type=LogEntryTypes.ERROR)

    def _summarize_errors(self, errors):
        error_dict = {}
        for error in errors:
            err_key = ' '.join(filter(None, [error.get('statusCode'), ', '.join(filter(None, error.get('fields'))),
                                             error.get('message') or error.content]))
            err_count = error_dict.get(err_key) or 0
            error_dict[err_key] = err_count + 1
        return error_dict

    def _write(self, job):
        results = {}
        label_wrapped = ' (' + job.get('label') + ')' if job.get('label') else ''
        print(("Running" + bcolors.OKGREEN + " {} {}" + bcolors.ENDC + "{}").format(job.get('series'),
                                                                                  job.get('level'), label_wrapped))
        print(("\t\t" + bcolors.OKGREEN + "{}" + bcolors.ENDC + " on " + bcolors.OKGREEN + "{}" + bcolors.ENDC +
              " from " + bcolors.OKCYAN + "{}" +
               bcolors.ENDC).format(job.get('operation'), job.get('sf_object'), job.get('query')))
        start = time.time()
        for repeat in range(job.get('run_x_times', 1)):
            try:
                if repeat > 0:
                    print('Repeating job run {} out of {} times'.format(repeat+1, job.get('run_x_times')))
                if job.get('query') and job.get('operation') != 'sql':
                    try:
                        loader = SalesforceDataLoader(self._config)
                        results = loader.load_view(job) or {}
                        if results and results.get('errors'):
                            raise RecordErrorException('Job processed with record errors.')
                        elif results:
                            self._logger.log(
                                f"""Job {job.get('level')} completed ({job.get('sf_object')} {job.get('operation')}).""",
                                type=LogEntryTypes.INFO)
                            results['status'] = JobResult.COMPLETED
                        else:
                            results = {'status': JobResult.FAILED}

                    except RecordErrorException as e:
                        self._logger.log(f"""Job {job.get('level')} completed with errors ({job.get('sf_object')} {job.get('operation')}).""", type=LogEntryTypes.ERROR)
                        self._log_errors(results.get('errors'))
                        results['status'] = JobResult.ERRORS
                    except ProgrammingError as e:
                        self._logger.log(f"""Job {job.get('level')} failed with SQL statement error ({job.get('sf_object')} {job.get('operation')}).\n{e}""", type=LogEntryTypes.ERROR)
                        results = {'status': JobResult.FAILED}

                if not job.get('skip_reload') and not job.get('validate_only') and job.get('operation') != 'sql':
                    self.read_by_objects([job.get('sf_object')])
                    indirectly_updates = job.get('indirectly_updates')
                    if indirectly_updates:
                        indirectly_updates = [x.strip() for x in indirectly_updates.split(',')]
                        self.read_by_objects(indirectly_updates)
            except Exception as e:
                exc_type, value, traceback = sys.exc_info()
                self._logger.log(traceback, type=LogEntryTypes.ERROR)
                results['status'] = JobResult.FAILED

        end = time.time()
        print('End Time: {} \t Elapsed Time: {}'.format(time.strftime('%H:%M:%S', time.localtime(end)),
                                                      time.strftime('%H:%M:%S', time.gmtime(end - start))))
        return results

    def load_by_object(self, objname):
        self._config.reload()
        filtered_jobs = [d for d in self._config.jobs if d['sf_object'] == objname]
        if not filtered_jobs:
            self._logger.logs(f"No load configurations found for {objname}", LogEntryTypes.ERROR)
        else:
            self._run_jobs(filtered_jobs)

    def load(self, min, max=None):
        self._config.reload()
        series = self._config.SALESFORCE_CONFIG.get('default_series')

        if series:
            self.load_by_series(series, min, max_level=max)

        else:
            print('Default Series not defined in config.')

    def load_by_series(self, series, start, max_level=None):
        self._config.reload()
        if not max_level:
            max_level = start

        filtered_jobs = [d for d in self._config.jobs if d['series'] == series and
                         start <= d['level'] <= max_level]
        sorted_jobs = sorted(filtered_jobs, key=lambda x: x.get('level'))
        if not sorted_jobs:
            print('WARNING: No load configurations found')
        self._run_jobs(sorted_jobs)

    def _run_jobs(self, jobs):
        for i, job in enumerate(jobs):
            if job.get('query') and job.get('operation') not in ['sql', 'reload']:
                results = self._write(job)
                if results.get('status') == JobResult.FAILED:
                    self._logger.log('Job FAILED. Aborting run.', type=LogEntryTypes.ERROR)
                    break

                if results.get('status') != JobResult.COMPLETED:
                    action = job.get('on_exception_record_error', 'abort')
                    last_job = ((i + 1) == len(jobs))
                    if action == 'abort' or (action == 'prompt' and not last_job and
                                             not yes_or_no('Job had record errors. Continue?')):
                        self._logger.log('Run aborted by user.', LogEntryTypes.ERROR)
                        break

            if job.get('operation') == 'sql':
                self._sql_tools.sqlalchemy_connect_to_db().execute(job.get('query'))

            if job.get('operation') == 'reload':
                self.read_by_objects(job.get('sf_object'))
        self._logger.log('Jobs completed.', type=LogEntryTypes.INFO)

    def main(self, object_or_list_of_objects):
        filtered_loads = {k: v for k, v in self._config.reads.items() if k in object_or_list_of_objects}

    def switch_orgs(self, sandbox=None):
        auth = SalesforceAuth(self._config)
        auth.switch_orgs(sandbox)

    def open_sf(self):
        self._sf_tools.open_sf_url()

    def get_schema(self, object_filters=None):
        return self._sf_tools.get_schema(object_filters)

    def schema_to_csv(self, output_file='schema.csv', object_filters=None):
        df = self._sf_tools.get_schema(object_filters)
        df.to_csv(output_file, index=False)
        print(f"Saved to {output_file}")
        return df

    def export_schema_to_sql(self, table_name='Z_SF_Schema', object_filters=None):
        df = self._sf_tools.get_schema(object_filters)
        con = self._sql_tools.sqlalchemy_connect_to_db()
        df.to_sql(table_name, con, if_exists='replace', index=False)
        return df



def init():
    cfg = Config('../../')
    r = Runner(cfg)
    return r

if __name__ == "__main__":
    init()


