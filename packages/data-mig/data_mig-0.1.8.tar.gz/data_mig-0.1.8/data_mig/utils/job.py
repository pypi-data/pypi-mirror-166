from data_mig.sql.loader import SQLDataLoader
from data_mig.salesforce.tools import SalesforceTools
class Job(object):
    """      label: 'Contact'
      sf_object: 'Contact'
      query: 'SELECT * FROM ADDR_PRIMARY_CONTACT'
      operation: 'upsert'
      filter_invalid: True
      #only drop audit on second run for updates in order to import new contacts with created date.
      drop_audit_on_upsert: True
      id: 'Id'"""
    label = None
    query = None
    output_module = None
    input_module = None
    operation = None
    filters = []
    parameters = {}

    def __init__(self, label=None, query=None, destination=None, data):

class SalesforceToSQL(Job):

    def __init__(self, config, query, **kwargs):
        self.input_module = SalesforceTools(config)#.query_to_dataframe(query, query_all=kwargs.get('query_all'))
        self.output_module = SQLDataLoader(config).load_dataframe(df, dest_table=None, if_exists='replace', )
        self.query = query

    def exec(self):
        input = self.output_module

