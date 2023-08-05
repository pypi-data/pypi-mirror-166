from simple_salesforce import Salesforce, exceptions as SS_Exception
import pandas as pd
import datetime
from urllib.parse import urlparse
from data_mig.sql.tools import SQLTools
from data_mig.salesforce.oauth import SalesforceAuth
from data_mig.salesforce.bulk import CustomBulkHandler
import json
import progressbar

DEFAULT_SALESFORCE_VERSION = 53.0


class SalesforceTools(object):
    def __init__(self, config):
        self._config = config
        self._sf_config = config.SALESFORCE_CONFIG
        self._oauth = SalesforceAuth(config)
        self.sf_api = None
        if not config.SALESFORCE_CONFIG.get('access_token') or not config.SALESFORCE_CONFIG.get('refresh_token'):
            self.refresh_token()
        self.connect()

    def bulk_api(self, sf_object):
        return getattr(CustomBulkHandler(self.sf_api.session_id, self.sf_api.bulk_url), sf_object)

    def refresh_token(self):
        self._oauth.refresh_token()

    def connect(self):
        config = self._config
        if not self.sf_api:
            instance = urlparse(config.SALESFORCE_CONFIG.get('instance_url')).hostname
            self.sf_api = Salesforce(instance=instance, session_id=config.SALESFORCE_CONFIG.get('access_token', ''),
                                     version=config.SALESFORCE_CONFIG.get('sf_version', DEFAULT_SALESFORCE_VERSION))

        try:
            self.sf_api.describe()
        except (SS_Exception.SalesforceMalformedRequest, SS_Exception.SalesforceExpiredSession):
            print('Refreshing Token')
            self.refresh_token()
            instance = urlparse(config.SALESFORCE_CONFIG.get('instance_url')).hostname
            self.sf_api = Salesforce(instance=instance, session_id=config.SALESFORCE_CONFIG.get('access_token'),
                                     version=config.SALESFORCE_CONFIG.get('sf_version', DEFAULT_SALESFORCE_VERSION))

        return self.sf_api

    def get_org_info(self):
        if not self.sf_api:
            self.connect()
        resp = self.sf_api.restful('query', params={
            "q": "SELECT Id, InstanceName, IsSandbox, OrganizationType FROM Organization"})
        return resp.get('records')[0]

    def query(self, query, query_all=False):
        self.sf_api = self.connect()
        sf_object = SQLTools.get_table_from_query(query)

        bulk_api = getattr(CustomBulkHandler(self.sf_api.session_id, self.sf_api.bulk_url), sf_object)

        if query_all:
            bulk_api_query = bulk_api.query_all
        else:
            bulk_api_query = bulk_api.query

        return bulk_api_query(query, lazy_operation=False)

    def query_to_dataframe(self, query, query_all=False):
        results = self.query(query, query_all=query_all)
        output = []
        sf_object = SQLTools.get_table_from_query(query)
        for row in results:
            output.append(self._expand_related_fields(row))

        df = pd.DataFrame.from_dict(output)
        df = df.drop(labels=['attributes'], axis='columns', errors='ignore')
        df = self._fix_datetimes_using_schema(df, sf_object)
        return df

    def _fix_datetimes_using_schema(self, df, sf_object):
        sf_field_schema = self.get_object_fields(sf_object)
        datetime_fields = []

        for field in df.columns:
            fs = sf_field_schema.get(field)  # TODO: Handle datetime fields on relationship fields
            if fs and fs.get('type') == 'datetime':
                datetime_fields.append(field)

        for f in datetime_fields:
            df[f] = df[f].map(SalesforceTools._convert_timestamp_utc)

        return df

    @staticmethod
    def _convert_timestamp_utc(timestamp_int):
        try:
            return datetime.datetime.fromtimestamp(timestamp_int / 1000)
        except (ValueError, TypeError):
            return None

    def _expand_related_fields(self, dict):
        output = dict.copy()
        for field, value in dict.items():
            try:
                if value and 'attributes' in value:
                    for related_field, rf_value in value.items():
                        try:
                            output += self._expand_related_fields(rf_value)
                        except(TypeError, AttributeError):
                            if related_field not in ['attributes']:
                                output['{}.{}'.format(field, related_field)] = rf_value
                    output.pop(field, None)
                    output.pop('attributes', None)
            except (TypeError, UnicodeEncodeError, AttributeError) as e:
                pass
        return output

    def get_object_schema(self, objName):
        self.sf_api = self.connect()
        objectSFType = getattr(self.sf_api, objName)
        describe = objectSFType.describe()
        return describe

    def get_object_fields(self, objName):
        salesforce_fields = self.get_object_schema(objName).get('fields')
        sf_field_metadata = {}
        for field in salesforce_fields:
            field_metadata = field
            field_metadata['required'] = not field.get('nillable') \
                                         and field.get('updateable') \
                                         and field.get('createable')\
                                         and not field.get('defaultedOnCreate')
            field_metadata['formula'] = field.get('calculatedFormula')

            sf_field_metadata[field.get('name')] = field_metadata
        return sf_field_metadata

    def get_required_fields(self, objName):
        fields = self.get_object_fields(objName)
        return dict([(k, v) for k, v in fields.items() if v.get('required')])

    def get_schema(self, object_filters=None):
        if not object_filters:
            object_filters = {'createable': True, 'customSetting': False, 'layoutable': True}
        objects = self.sf_api.describe()["sobjects"]
        schema = []
        for obj in progressbar.progressbar(objects):
            if all(obj[key] == value for key, value in object_filters.items()):
                object_name = obj['name']
                fields = self.get_object_fields(object_name)
                for name, details in fields.items():

                    label = details.get('label')
                    type = details.get('type')
                    type_with_details = type
                    help_text = details.get('inlineHelpText')
                    formula = details.get('formula')
                    required = details.get('required')
                    external_id = details.get('externalId')
                    length = details.get('length')
                    precision = details.get('precision')
                    scale = details.get('scale')
                    updateable = details.get('updateable')
                    createable = details.get('createable')
                    restrictedPicklist = details.get('restrictedPicklist')
                    calculated = details.get('calculated')
                    nillable = details.get('nillable')
                    picklist_values = []
                    for pvalue in details.get('picklistValues'):
                        if pvalue.get('active'):
                            if pvalue.get('label'):
                                picklist_values.append(pvalue.get('label'))

                    picklist_values = ";".join(picklist_values)

                    attributes = []

                    if precision > 0 or scale > 0:
                        length_or_number_size = f"{precision}, {scale}"
                        type_with_details = f"{type} ({length_or_number_size})"

                    if type == 'reference':
                        reference_to = ';'.join(details.get('referenceTo'))
                        type_with_details = f"{type} ({reference_to})"
                        type = type_with_details

                    if picklist_values:
                        type_with_details = f"{type} ({picklist_values})"

                    if type == 'string' or type == 'textArea':
                        type_with_details = f"{type} ({length})"

                    # attribute flags
                    if external_id:
                        attributes.append('EXT ID')

                    if required:
                        attributes.append('REQUIRED')

                    if restrictedPicklist:
                        attributes.append('RESTRICTED')

                    if calculated:
                        attributes.append('CALCULATED')

                    if not updateable:
                        attributes.append('NOT UPDATEABLE')

                    if not createable:
                        attributes.append('NOT CREATEABLE')

                    if not nillable:
                        attributes.append('NOT NILLABLE')

                    if attributes:
                        type_with_details += ' ' + ' '.join(attributes)

                    row = {'Salesforce Field Key': f"{object_name}.{label}", 'Object': object_name,
                           'Field Label': label,
                           'API Name': name, 'Type with Details': type_with_details, 'Help Text': help_text,
                           'Formula': formula,
                           'Attributes': ';'.join(attributes), 'Type': type, 'Picklist Values': picklist_values,
                           'Details': json.dumps(details, skipkeys={'urls'}) }
                    schema.append(row)

        df = pd.DataFrame(schema)
        return df

    def open_sf_url(self, url=None, relative_url=None):
        self._oauth.open_sf_url(url=url, relative_url=relative_url)

    def is_email_enabled(self):
        email_status = self.sf_api.restful('tooling/executeAnonymous', {'anonymousBody': """
            System.debug('Fionta / Arroyo checking email sending access');
            Messaging.reserveSingleEmailCapacity(1);
            Messaging.reserveMassEmailCapacity(1);
        """})

        return email_status['success']
