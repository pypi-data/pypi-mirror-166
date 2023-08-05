import pandas as pd
import numpy as np
import urllib.parse
import os
import sys
import re
import sqlalchemy.dialects.mssql as types
import sqlalchemy
from data_mig.sql.tools import SQLTools
from data_mig.utils.config import Config
from data_mig.jobs.runner import Runner


class CSVToSQLLoader(object):

	def __init__(self, config, path='../Staging Tables'):
		self._config  = config
		self._engine = SQLTools(config).sqlalchemy_connect_to_db()
		self._path = path
		self._dir = os.listdir(path)

	def load_all(self):
		self.load_csv()
		self.load_xlsx()
		self.load_txt()

	def load_dataframe(self, df):
		if 'id' in df.columns.values:
			df.to_sql('table_name', self._engine, index=False, if_exists='replace')
		else:
			df.to_sql('table_name', self._engine, index=True, index_label='id', if_exists='replace')


	def get_type(self, df_column):
		try:
			if df_column.dtype == 'object':
				df_column_length = df_column.str.len().max()
				if np.isnan(df_column_length):
					df_column_length = 100
				if df_column_length > 2000:
					return types.VARCHAR()
				else:
					return types.VARCHAR(int(df_column_length)+10)
			else:
				return types.VARCHAR(100)
		except(AttributeError):
			print('Type Attribute not found. Are there multiple columns with the same name?')

	def trim_column_names_for_oracle(self, df):
		for column in df.columns.values:
			if len(column) > 30:
				df.rename(columns={column: column[:30]}, inplace=True)
			elif column in ['File', 'Column']:
				df.rename(columns={column: '{}Name'.format(column).upper()}, inplace=True)
			else:
				df.rename(columns={column: column.upper()}, inplace=True)

		return df

	def override_datatypes_text_all(self, df):
		dtyp = {c: self.get_type(df[c]) for c in df.columns}
		print('Data Types found: {}'.format(dtyp))
		return dtyp

	def load_txt(self, skip=None, only=None):
		skip = skip or []
		include_file_regex = re.compile('([A-z0-9\-\s]+)\.txt')

		if only:
			files = only
		else:
			files = [f for f in self._dir if include_file_regex.match(f) and not (f in skip)]

		for file in files:

			if include_file_regex.match(file) and not (file in skip):
				df = pd.read_csv(r'{}/{}'.format(self._path, file), sep='\t', low_memory=False, parse_dates=False)
				if len(df) > 0:
					table_name = file.replace('.txt', '').replace('(', '_').replace(')', '_').replace(' ', '_').lower()
					# dtyp = override_datatypes_text_all(df)
					print('Loading {} as {}'.format(file, table_name))
					df.to_sql(table_name, self._engine, index=False, if_exists='replace')

	def load_csv(self, skip=None, only=None):
		skip = skip or []
		include_file_regex = re.compile('([A-z0-9\-\s]+)\.csv')

		if only:
			files = only
		else:
			files = [f for f in self._dir if include_file_regex.match(f) and not (f in skip)]

		for file in files:

			if include_file_regex.match(file) and not (file in skip):  # and (file in only):
				print('reading file {}'.format(file))
				df = pd.read_csv(r'{}/{}'.format(self._path, file), sep=',', low_memory=False, parse_dates=False, dtype=str)
				print(df)
				if len(df) > 0:
					table_name = file.replace('.csv', '').replace('(', '_').replace(')', '_').replace(' ', '_').lower()
					dtyp = self.override_datatypes_text_all(df)
					print('Loading {} as {}'.format(file, table_name))
					df.to_sql(table_name, self._engine, index=False, if_exists='replace', dtype=dtyp)

	def load_xlsx(self, skip=None, only=None):
		skip = skip or []
		include_file_regex = re.compile('([A-z0-9\s]+)\.xlsx')

		if only:
			files = only
		else:
			files = [f for f in self._dir if include_file_regex.match(f) and not (f in skip)]

		for file in files:
			file_name_match = include_file_regex.match(file)
			if file_name_match:
				file_name = '{}/{}'.format(self._path, file)
				print('Loading file: {}'.format(file_name))
				xl = pd.ExcelFile(file_name)
				for sheet in xl.sheet_names:
					df = pd.read_excel(file_name, sheet_name=sheet, na_values='NULL')  # , dtype=str, encoding='UTF-8'
					pd.set_option('display.max_colwidth', 1000)
					df = df.replace('nan', '')
					# print df
					table_name = '{}_{}'.format(file_name_match.group(1), sheet).replace('(', '_').replace(')',
																										   '_').replace(
						' ', '_').lower()
					print('Loading sheet: {}'.format(table_name))
					# df = trim_column_names_for_oracle(df)
					dtyp = self.override_datatypes_text_all(df)
					df.to_sql(table_name, self._engine, index=False, if_exists='replace')  # , dtype=dtyp)



if __name__ == "__main__":
   load_xlsx()
   load_csv()
   runner = Runner(config)
   runner.read_all()
