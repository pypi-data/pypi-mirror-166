from data_mig.salesforce.tools import *
from data_mig.sql.tools import *
from sqlalchemy import exc

#import sqlalchemy.dialects.mssql as types
import sqlalchemy.types as types
import numpy as np
import time

NUMPY_TO_SQLALCHEMY_DATATYPES = {
    'int64': types.BIGINT,
    'float64': types.FLOAT,
    'object': types.NVARCHAR,
    'datetime': types.DATETIME,
    'datetime64': types.DATETIME,
    'datetime64[ns]': types.DATETIME,
    'bool': types.SMALLINT
}

DEFAULT_DEST_PREFIX = 'SF_'
DEFAULT_SQL_CHUNK_SIZE = 10000


class SQLDataLoader(object):

    def __init__(self, config, salesforce_query, destination_table=None, query_all=False, indexes=None,
                 post_read_query=None, chunksize=None, if_exists='replace', method=None, destination_table_prefix=None):
        self._config = config
        self.sql_tools = SQLTools(config)
        self._query = salesforce_query.replace('\n', '').replace('\r', '')
        if destination_table:
            self._destination_table = destination_table
        else:
            qry = self.sql_tools.get_table_from_query(salesforce_query)
            self._destination_table = (destination_table_prefix or DEFAULT_DEST_PREFIX) + qry
        self._data = None
        self._indexes = indexes
        self._method = method
        self._if_exists = if_exists or 'replace'
        self._post_read_query = post_read_query
        self._chunksize = chunksize or DEFAULT_SQL_CHUNK_SIZE
        self._query_all = query_all

    def __repr__(self):
        return "SQLDataLoader()"

    def __str__(self):
        return 'Query: {}\nDestination Table: {}'.format(self._query, self._destination_table)

    def load(self):
        sf = SalesforceTools(self._config)
        df = sf.query_to_dataframe(self._query, query_all=self._query_all)
        if df.shape[1] > 0:
            self.load_dataframe(df, indexes=self._indexes, chunksize=self._chunksize,
                                method=self._method, if_exists=self._if_exists)
        else:
            columns = self.sql_tools.get_fields_from_query(self._query)
            print("No records found. Creating dummy record to setup table.")
            self.load_dataframe(pd.DataFrame([[None for i in range(len(columns))]], columns=columns))

    def load_dataframe(self, df, dest_table=None, if_exists='replace', indexes=None,
                       chunksize=None, method=None):
        dest_table = dest_table or self._destination_table
        conn = self.sql_tools.sqlalchemy_connect_to_db()
        dtypes = self._override_datatypes_text_all(df)
        if not df.empty:
            print("Loading {} records into {}".format(df.shape[0], dest_table))
            # print('Advanced params: {{ chunksize: {}, method: {}, indexes: {} }}'.format(chunksize, method, indexes))
            try_number = 1
            retry = True
            while retry:
                try:
                    if try_number == 2:
                        method = None
                        chunksize = DEFAULT_SQL_CHUNK_SIZE
                    if try_number >= 3:
                        chunksize = chunksize / 2
                    if try_number >= 4:
                        retry = False
                    df.to_sql(dest_table, con=conn, if_exists=if_exists, index=False, dtype=dtypes,
                              chunksize=chunksize or self._chunksize, method=method)
                    retry = False
                except (exc.SQLAlchemyError, exc.OperationalError, exc.DBAPIError) as e:
                    print("SQL Alchemy Exception Caught")
                    print(e)
                    try_number = try_number + 1

            if indexes:
                self.create_indexes(dest_table, indexes.split(','))

            if self._config.DATABASE_CONFIG.get('POST_READ_QUERY'):
                qry = self._config.DATABASE_CONFIG.get('POST_READ_QUERY')
                print('Executing POST_READ_QUERY: {}'.format(qry))
                from sqlalchemy import text
                results = conn.execute(text(qry).execution_options(autocommit=True))
                time.sleep(60)

            if self._post_read_query:
                qry = self._post_read_query
                print('Executing job-based POST_READ_QUERY: {}'.format(qry))
                from sqlalchemy import text
                results = conn.execute(text(qry).execution_options(autocommit=True))
                time.sleep(60)

        else:
            print("No records found to load.")

    def create_indexes(self, dest_table, indexes):
        conn = self.sql_tools.sqlalchemy_connect_to_db()
        for idx in indexes:
            conn.execute('CREATE INDEX idx_{} on {} ({});'.format(idx.strip(), dest_table, idx.strip()))

    def _override_datatypes_text_all(self, df):
        dtyp = {c: self._get_type(df[c]) for c in df.columns}
        # print('Data Types found: {}'.format(dtyp))
        return dtyp

    def _get_type(self, df_column):
        mapped_dtype = NUMPY_TO_SQLALCHEMY_DATATYPES.get(str(df_column.dtype))
        try:
            if df_column.dtype == 'object':
                df_column_length = df_column.str.len().max()
                if np.isnan(df_column_length):
                    df_column_length = 245
                if df_column_length <= 3900:
                    return types.NVARCHAR(str(int(round(df_column_length + 10))))
                else:
                    return types.NVARCHAR('max')

            else:
                return mapped_dtype
        except AttributeError as e:
            print('Type Attribute not found. Are there multiple columns with the same name?')
