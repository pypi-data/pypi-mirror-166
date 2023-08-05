import pyodbc
from sqlalchemy import create_engine
from string import Template
import urllib
import re
from data_mig.utils.caseinsensitivelist import *
import numpy as np
import pandas as pd
from data_mig.utils.logging import bcolors, Logging, LogEntryTypes
import sqlparse
from sqlparse.tokens import Keyword, DML, Whitespace

class SQLTools(object):

    def __init__(self, config):
        self._config = config
        self._sqlalchemy_engine = None
        self._sqlalchemy_connection = None
        self._logger = Logging(config).log

    def sqlalchemy_connection_string(self):
        connection_variables = {k: urllib.parse.quote_plus(str(v)) for k, v in self._config.DATABASE_CONFIG.items()}
        if not connection_variables.get('PWD'):
            connection_template = "${SERVER}/${DATABASE}?driver=${DRIVER}&MARS_Connection=Yes&&Encrypt=yes&TrustServerCertificate=Yes&ssl=True&Trusted_Connection=yes"
        else:
            connection_template = "${UID}:${PWD}@${SERVER}:${PORT}/${DATABASE}?driver=${DRIVER}&MARS_Connection=Yes&&Encrypt=yes&TrustServerCertificate=Yes&ssl=True"
        connection_variables['DRIVER'] = connection_variables['DRIVER'].replace('%7D', '').replace('%7B', '')
        connection_variables['PORT'] = connection_variables.get('PORT', 1433)
        connection_string = "mssql+pyodbc://" + Template(connection_template).substitute(**connection_variables)
        return connection_string

    def sqlalchemy_connect_to_db(self, reset=False):
        if reset or not self._sqlalchemy_connection:
            #connection string without DSN:
            echo = self._config.DATABASE_CONFIG.get('ECHO', False)
            encoding = self._config.DATABASE_CONFIG.get('ENCODING', 'utf-8')
            self._sqlalchemy_engine = create_engine(self.sqlalchemy_connection_string(),
                                              echo=echo, encoding=encoding, isolation_level='READ_UNCOMMITTED',
                                                    fast_executemany=True, pool_pre_ping=True)

            self._sqlalchemy_connection = self._sqlalchemy_engine.connect()

        return self._sqlalchemy_connection

    def query_to_dataframe(self, query, silent=False):
        from pyodbc import ProgrammingError
        conn = self.sqlalchemy_connect_to_db()
        result = conn.execute(query)
        data = result.fetchall()
        result.close()
        return pd.DataFrame(data, columns=result.keys())

    @staticmethod
    def build_mssql_insert_with_bind_vars(column_names, destination_table_name):
        insert_columns = []
        insert_bind_vars = []
        bind_var_no = 1
        for field in column_names:
            insert_columns.append(field)
            insert_bind_vars.append('?')
            bind_var_no = bind_var_no + 1

        ins_query = 'INSERT INTO {} ({}) VALUES ({})'.format(destination_table_name, '['+('], ['.join(column_names))+']'.upper(),
                                                             ', '.join(insert_bind_vars))
        return ins_query

    @staticmethod
    def build_sql_insert_values_from_sf_data(column_names, data_to_insert):
        insert_values = []
        for record in data_to_insert.get('records'):
            record = CaseInsensitiveList(record)
            sf_values = []
            for key in column_names:
                split_key = key.split('.')
                value = None
                if len(split_key) == 2 and record.get(split_key[0]):
                    value = record.get(split_key[0]).get(split_key[1])
                else:
                    value = record.get(split_key[0])
                sf_values.append(value)

            insert_values.append(tuple(sf_values))

        return insert_values

    @staticmethod
    def check_destination_column_lengths(insert_column_names, insert_values, dest_column_metadata):

        length = lambda y: len(y) if y else 0

        lengths = []
        for x in insert_values:
            lengths.append([length(y) for y in x])

        np_lengths = np.array(lengths)
        max_lengths = np_lengths.max(axis=0)

        i = 0
        max_by_column = {}

        for x in insert_column_names:
            max_by_column[x] = max_lengths[i]
            i += 1

        dest_column_lengths = {x['name']: SQLTools.get_length_from_sql_type(x['type']) for x in dest_column_metadata}

        for (k, v) in max_by_column.items():
            dest_length = dest_column_lengths.get(k)
            if dest_length and v > dest_length:
                raise Exception('Error: Source field {} length ({}) is larger than destination field length ({})'.format(k, v, dest_length))

    @staticmethod
    def get_fields_from_query(query):
        try:
            limit_re = re.search('TOP \d+', query, re.IGNORECASE)
            limit_text = limit_re.group(0)
            query = query.replace(limit_text, '')
        except AttributeError:
            pass

        sql = sqlparse.parse(query)[0]
        select_tokens = []
        skipping = False
        for token in sql.tokens:
            if token.match(Keyword, 'from'):
                skipping = True
            if token.ttype not in [DML, Whitespace] and not skipping:
                select_tokens.append(token.value)
        output = []
        for o in select_tokens:
            output.extend(o.replace(' ', '').replace('\n', '').split(','))
        return output

    @staticmethod
    def get_table_from_query(query):
        p = re.compile(r"(?<=FROM) (\w+)", re.IGNORECASE | re.MULTILINE)
        m = p.search(query)
        try:
            fields_from_query = m.group(1)
        except IndexError:
            return None
        return fields_from_query

    @staticmethod
    def get_length_from_sql_type(sql_type):
        try:
            return sql_type.length
        except (KeyError, AttributeError) as e:
            return None

    @staticmethod
    def result_count_query(query):
        query_template = "SELECT COUNT(*) "
        try:
            limit_re = re.search('TOP \d+', query, re.IGNORECASE)
            limit_text = limit_re.group(0)
            query = query.replace(limit_text, '')
            query_template = Template("SELECT $limit COUNT(*) ").substitute(limit=limit_text)
        except AttributeError:
            pass

        sql = sqlparse.parse(query)[0]

        output = [query_template]

        skipping = True
        for token in sql.tokens:
            if token.match(Keyword, 'from'):
                skipping = False
            if not skipping:
                output.append(token.value)
        return "".join(output)

