from data_mig.sql.tools import *
from data_mig.utils.config import Config
from data_mig.salesforce.tools import SalesforceTools
from data_mig.sql.loader import SQLDataLoader
import pandas as pd

cfg = Config(path='../../../')
def test_query():
    sf_query = 'SELECT Id, Subject, ActivityDate, Who.Name FROM TASK'
    sql = SQLDataLoader(cfg, sf_query, query_all=True)
    sql.load()


if __name__ == '__main__':
    test_query()
