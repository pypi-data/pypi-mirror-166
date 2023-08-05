from __future__ import print_function
from data_mig.salesforce.tools import SalesforceTools
from data_mig.salesforce.tools import CustomBulkHandler
from data_mig.utils.config import Config
import os
import zipfile
#import StringIO
import pandas as pd
import json
import copy

cfg = Config(path='../../..')
sf_tools = SalesforceTools(cfg)
sf_api = sf_tools.connect()

attachment_bulk_api = getattr(CustomBulkHandler(sf_api.session_id, sf_api.bulk_url), 'Attachment')
attachment_bulk_operation = getattr(attachment_bulk_api, 'insert')

files_bulk_api = getattr(CustomBulkHandler(sf_api.session_id, sf_api.bulk_url), 'ContentVersion')
files_bulk_operation = getattr(files_bulk_api, 'insert')


# Credit to: https://stackoverflow.com/questions/2463770/python-in-memory-zip-library
class InMemoryZip(object):
    def __init__(self):
        # Create the in-memory file-like object
        self.in_memory_zip = StringIO.StringIO()
        self._in_memory_zip_previous = StringIO.StringIO()

    def _backup(self):
        self._in_memory_zip_previous = StringIO.StringIO()
        self._in_memory_zip_previous.write(self.in_memory_zip.getvalue())

    def append(self, filename_in_zip, file_contents):
        '''Appends a file with name filename_in_zip and contents of
        file_contents to the in-memory zip.'''
        # backup in memory zip
        self._backup()

        # Get a handle to the in-memory zip in append mode
        zf = zipfile.ZipFile(self.in_memory_zip, "a", zipfile.ZIP_DEFLATED, False)

        # Write the file to the in-memory zip
        zf.writestr(filename_in_zip, file_contents)

        # Mark the files as having been created on Windows so that
        # Unix permissions are not inferred as 0000
        for zfile in zf.filelist:
            zfile.create_system = 0

        return self

    def revert(self):
        self.in_memory_zip = StringIO.StringIO()
        self.in_memory_zip.write(self._in_memory_zip_previous.getvalue())

    def read(self):
        '''Returns a string with the contents of the in-memory zip.'''
        self.in_memory_zip.seek(0)
        return self.in_memory_zip.read()

    def writetofile(self, filename):
        '''Writes the in-memory zip to a file.'''
        f = file(filename, "w")
        f.write(self.read())
        f.close()

    def close(self):
        self.in_memory_zip = StringIO.StringIO()

    def __len__(self):
        return self.in_memory_zip.len


class BatchFullException(Exception):
    pass


class BatchClosedException(Exception):
    pass


class SalesforceBinaryAttachmentBatch(object):
    ADJ_FOR_REQUEST = 10*1024
    BATCH_UNCOMPRESSED_LIMIT = (20 * 1024**2) - ADJ_FOR_REQUEST
    BATCH_ZIP_FILE_LIMIT = (10 * 1000**2) - ADJ_FOR_REQUEST
    IGNORED_FILES = ['request.csv', '.DS_Store']
    uncompressed_file_size = 0
    batch_request_data = []

    def __init__(self):
        self.zip = InMemoryZip()
        self.batch_request_data = []
        self.closed = False

    def append(self, filename_in_zip, file_contents, request_data):
        if self.closed:
            raise BatchClosedException('Batch is already closed.')

        filesize = len(file_contents)
        if self.uncompressed_file_size + filesize > self.BATCH_UNCOMPRESSED_LIMIT:
            raise BatchFullException('Adding {} would exceed uncompressed file size limit ({}).'.format(filename_in_zip, self.BATCH_UNCOMPRESSED_LIMIT))

        self.zip.append(filename_in_zip, file_contents)

        if self.len() > self.BATCH_ZIP_FILE_LIMIT:
            self.zip.revert()
            raise BatchFullException('Adding {} would exceeds compressed batch size limit.'.format(filename_in_zip, self.BATCH_ZIP_FILE_LIMIT))

        self.batch_request_data.append(request_data)

    def close(self):
        if not self.closed:
            self.zip.append('request.txt', json.dumps(self.batch_request_data, allow_nan=False, skipkeys=True))
            self.closed = True

    def read(self):
        return self.zip.read()

    def len(self):
        return len(self.zip)

    def __str__(self):
        status = 'Open' if not self.closed else 'Closed'
        zip_summary = ''
        try:
            zf = zipfile.ZipFile(self.zip.in_memory_zip, "r", zipfile.ZIP_DEFLATED, False)
            zip_summary = '\n'.join(zf.namelist())
            zip_request = zf.read('request.txt')
        except zipfile.BadZipfile:
            zip_summary = 'Empty'
            zip_request = self.batch_request_data

        summary = """Batch Status {}:
Request:
{}
Files:
{}""".format(status, zip_request, zip_summary)
        return summary

def get_job_request_from_csv(dir, filename='request.csv'):
    file_with_path = os.path.join(dir, filename)
    request = pd.read_csv(file_with_path, header=0, sep=',', encoding='UTF-8')
    request = request.to_dict(orient='records')
    for r in request:
        for key, value in r.items():
            if value is None:
                del d[key]
    return request


def get_attachment_batch():
    IGNORED_FILES = ['request.csv', '.DS_Store']
    uncompressed_file_size = 0
    directory = '/Users/dacmanj/Downloads/attachments'
    batch = SalesforceBinaryAttachmentBatch()
    job_request = get_job_request_from_csv(directory)


    for f in job_request:
        filename = f.get('Body')[1:]
        file_with_path = os.path.join(directory, filename)
        file = open(file_with_path, 'r')

        try:
            batch.append(filename, file.read(), f)
        except BatchFullException:
            batch.close()
            yield batch
            batch = SalesforceBinaryAttachmentBatch()
            batch.append(filename, file.read(), f)

    batch.close()
    yield batch




class FileJobRequest(object):
    CONTENT_VERSION_KEYS = ['VERSIONDATA', 'PATHONCLIENT', 'TITLE', 'DESCRIPTION', 'TAGCSV', 'RECORDTYPEID']
    def __init__(self, dir, filename='request.csv'):
        self.request = self._get_job_request_from_csv(dir, filename)

    def _get_job_request_from_csv(self, dir, filename='request.csv'):
        file_with_path = os.path.join(dir, filename)
        self.request = pd.read_csv(file_with_path, header=0, sep=',', encoding='UTF-8')
        self.request.
        self.request = self.request.to_dict(orient='records')
        self.request = [dict((k.upper(), v) for k in self.request)]

        return request

    def to_sf_dict(self):

        output = copy.copy(self.request)
        for r in self.request:
            for key, value in r.items():
                if value is None or key.upper() not in self.CONTENT_VERSION_KEYS:
                    del d[key]
        return output

    def update_file(self, filename, attr_name, attr_value):
        file_match = [r for r in result if r.get('PATHONCLIENT') == filename]
        for f in file_match:
            f[attr_name] = attr_value

    #assuming file/path uniqueness
    def get_file(self, filename):
        file_match = [r for r in result if r.get('PATHONCLIENT') == filename]
        return file_match[0]

def get_files_batch(job_data):
    IGNORED_FILES = ['request.csv', '.DS_Store']
    uncompressed_file_size = 0
    batch = SalesforceBinaryAttachmentBatch()
    sf_data = job_data.to_dict()

    for f in sf_data:
        filename = f.get('PathOnClient')
        file_with_path = os.path.join(directory, filename)
        file = open(file_with_path, 'r')

        try:
            batch.append(filename, file.read(), f)
        except BatchFullException:
            batch.close()
            yield batch
            batch = SalesforceBinaryAttachmentBatch()
            batch.append(filename, file.read(), f)

    batch.close()
    yield batch

directory = '/Users/dacmanj/Downloads/files'
job_request = FileJobRequest(directory)
content_version_ids = []
for b in get_files_batch():
    print('Sending batch.')
    print(b)
    result = files_bulk_operation(b.read())

