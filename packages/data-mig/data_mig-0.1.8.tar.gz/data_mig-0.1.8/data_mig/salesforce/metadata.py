from data_mig.salesforce.tools import SalesforceTools
from zeep import Client
from zeep.transports import Transport
import requests
import importlib.resources as pkg_resources
from data_mig.salesforce import wsdl  # relative-import the *package* containing the templates

METADATA_NAMESPACE = 'http://soap.sforce.com/2006/04/metadata'


class MetadataAPI:
    def __init__(self, config):
        self._config = config
        self._sf_tools = SalesforceTools(self._config)
        self._sf_api = self._sf_tools.connect()
        # this needs to sync up with cached WSDL
        self._sf_version = 55.0
        self._session_id = self._config.SALESFORCE_CONFIG['access_token']
        self._soap_headers = {'SessionHeader': {'sessionId': self._session_id}}

        # WSDL now requires a nonce to retrieve. These can be obtained from
        # instance url + /services/wsdl/tooling or
        # /services/wsdl/metadata
        with requests.Session() as s:
            transport = Transport(session=s)
            metadata_wsdl = pkg_resources.open_binary(wsdl, 'metadata.xml')
            tooling_wsdl = pkg_resources.open_binary(wsdl, 'tooling.xml')

            self.metadata = Client(metadata_wsdl, transport=transport)
            self._metadata_endpoint = '{}/services/Soap/m/{}'.format(self._config.SALESFORCE_CONFIG['instance_url'],
                                                                     self._sf_version)

            self.metadata_service = self.metadata.create_service('{{{}}}MetadataBinding'.format(METADATA_NAMESPACE),
                                                                 self._metadata_endpoint)
            self.metadata._default_soapheaders = self._soap_headers

            self._tooling_endpoint = '{}/services/Soap/T/{}'.format(self._config.SALESFORCE_CONFIG['instance_url'],
                                                                    self._sf_version)
            self.tooling = Client(tooling_wsdl, transport=transport)
            self.tooling.set_default_soapheaders(self._soap_headers)
            self.tooling_service = self.tooling.create_service('{urn:tooling.soap.sforce.com}SforceServiceBinding',
                                                               self._tooling_endpoint)

    def list_metadata(self, *argv, **kwargs):
        kwargs['_soapheaders'] = self._soap_headers
        return self.metadata_service.listMetadata(*argv, **kwargs)

    def read_metadata(self, *argv, **kwargs):
        kwargs['_soapheaders'] = self._soap_headers
        return self.metadata_service.readMetadata(*argv, **kwargs)

    def create_metadata(self, *argv, **kwargs):
        kwargs['_soapheaders'] = self._soap_headers
        return self.metadata_service.createMetadata(*argv, **kwargs)

    def update_metadata(self, *argv, **kwargs):
        kwargs['_soapheaders'] = self._soap_headers
        return self.metadata_service.updateMetadata(*argv, **kwargs)

    def upsert_metadata(self, *argv, **kwargs):
        kwargs['_soapheaders'] = self._soap_headers
        return self.metadata_service.upsertMetadata(*argv, **kwargs)

    def delete_metadata(self, *argv, **kwargs):
        kwargs['_soapheaders'] = self._soap_headers
        return self.metadata_service.deleteMetadata(*argv, **kwargs)

    def describe_metadata(self, *argv, **kwargs):
        kwargs['_soapheaders'] = self._soap_headers
        return self.metadata_service.describeMetadata(*argv, **kwargs)

    def get_type(self, sf_type, namespace=METADATA_NAMESPACE):
        return self.metadata.get_type('{{{}}}{}'.format(namespace, sf_type))

    def get_element(self, sf_type, namespace=METADATA_NAMESPACE):
        return self.metadata.get_element('{{{}}}{}'.format(namespace, sf_type))


class MetadataWrapper:
    _md_api = None  # type: MetadataAPI
    VALID_FIELD_TYPES = ['AutoNumber', 'Lookup', 'MasterDetail', 'MetadataRelationship', 'Checkbox', 'Currency', 'Date',
                         'DateTime', 'Email', 'EncryptedText', 'Note', 'ExternalLookup', 'IndirectLookup', 'Number',
                         'Percent', 'Phone', 'Picklist', 'MultiselectPicklist', 'Summary', 'Text', 'TextArea',
                         'LongTextArea', 'Url', 'Hierarchy', 'File', 'Html', 'Location', 'Time']

    def __init__(self, config):
        self._sf_version = config.SALESFORCE_CONFIG['sf_version']
        self._md_api = MetadataAPI(config)

    def create_external_id_field(self, sf_obj):
        self.create_text_field(sf_obj, 'External_Import_Id__c', 'External Import Id',
                               externalId=True, unique=True, caseSensitive=False)

    def create_import_tag_field(self, sf_obj):
        self.create_text_field(sf_obj, 'Import_Tag__c', 'Import Tag',
                               externalId=True, unique=True, caseSensitive=False)

    def create_field(self, sf_obj, field_name, label, sf_type, **params):
        custom_field = self._md_api.get_type('CustomField')
        field_type = self._md_api.get_type('FieldType')
        my_cf = custom_field()
        my_cf.fullName = '{}.{}'.format(sf_obj, field_name)
        my_cf.label = label
        if sf_type not in self.VALID_FIELD_TYPES:
            raise InvalidFieldType(sf_type)
        my_cf.type = field_type(sf_type)
        # todo: iterate fields in CustomField from arg* param

    def create_text_field(self, sf_obj, field_name, label, length=255, external_id=False,
                          unique=False, caseSensitive=False):
        CustomField = self._md_api.get_type('CustomField')
        FieldType = self._md_api.get_type('FieldType')

        my_cf = CustomField()
        my_cf.fullName = '{}.{}'.format(sf_obj, field_name)
        my_cf.label = label
        my_cf.type = FieldType('Text')
        my_cf.externalId = external_id
        my_cf.unique = unique
        my_cf.caseSensitive = caseSensitive
        my_cf.length = length
        return self._md_api.create_metadata(my_cf)

    def add_field_permissions_to_profile(self, sf_obj, field, profile, editable=True, readable=True):
        Profile = self._md_api.get_type('Profile')
        p = Profile()
        p.fullName = profile
        perm = self.create_field_permission(sf_obj, field, editable, readable)
        p.fieldPermissions = [perm]
        self._md_api.update_metadata(p)

    def add_fields_to_profile(self, fields_and_permissions_to_add, profile, default_editable=True,
                              default_readable=True):
        Profile = self._md_api.get_type('Profile')
        p = Profile()
        p.fullName = profile
        p.fieldPermissions = []
        for field in fields_and_permissions_to_add:
            editable = field.get('editable', default_editable)
            readable = field.get('readable', default_readable)
            obj = field.get('object')
            field = field.get('field')
            perm = self.create_field_permission(obj, field, editable, readable)
            p.fieldPermissions.append(perm)
        print('Updating Profile {}'.format(p.fullName))
        self._md_api.update_metadata(p)

    def add_field_permissions_to_permission_set(self, sf_obj, field, permission_set, editable=True, readable=True):
        PermissionSet = self._md_api.get_type('PermissionSet')
        p = PermissionSet()
        p.fullName = permission_set
        perm = self.create_field_permission(sf_obj, field, editable, readable)
        p.fieldPermissions = [perm]
        self._md_api.update_metadata(p)

    def add_fields_to_permission_set(self, fields_and_permissions_to_add, permissionset, label, default_editable=True,
                                     default_readable=True):
        PermissionSet = self._md_api.get_type('PermissionSet')
        p = PermissionSet()
        p.fullName = permissionset
        p.label = label
        p.fieldPermissions = []
        for field in fields_and_permissions_to_add:
            editable = field.get('editable', default_editable)
            readable = field.get('readable', default_readable)
            obj = field.get('object')
            field = field.get('field')
            perm = self.create_field_permission(obj, field, editable, readable)
            p.fieldPermissions.append(perm)
        print('Updating PermissionSet {}'.format(p.fullName))
        self._md_api.update_metadata(p)

    def list_metadata(self, md_type, folder=None):
        ListMetadataQuery = self._md_api.get_type('ListMetadataQuery')
        md_query = ListMetadataQuery()
        md_query.type = md_type
        md_query.folder = folder
        md = self._md_api.list_metadata([md_query], self._sf_version)
        return md

    def list_metadata_full_names(self, md_type):
        return [x.fullName for x in self.list_metadata(md_type)]

    def read_metadata(self, md_type, names):
        md = self._md_api.read_metadata(md_type, names)
        return md

    def add_field_to_all_layouts(self, sf_obj, field_name):
        LayoutItem = self._md_api.get_type('LayoutItem')
        layouts = self.list_metadata('Layout')
        object_layouts = [x for x in layouts if x['fullName'].startswith(sf_obj)]
        for layout in object_layouts:
            layout_full_name = layout.fullName
            print('Adding {}.{} to {} layout'.format(sf_obj, field_name, layout_full_name))
            al = self._md_api.read_metadata('Layout', layout_full_name)
            al_layout_sections = al[0]['layoutSections']
            last_items = None

            for x in range(len(al_layout_sections) - 1, -1, -1):
                section = al_layout_sections[x]
                if not last_items and section.style != 'CustomLinks':
                    last_items = section['layoutColumns'][0]['layoutItems']

            item = LayoutItem()
            item.field = field_name
            item.behavior = 'Edit'
            last_items.append(item)
            self._md_api.update_metadata(al)

    def create_field_permission(self, sf_obj, field, editable, readable):
        PermissionSetFieldPermissions = self._md_api.get_type('PermissionSetFieldPermissions')
        p = PermissionSetFieldPermissions()
        p.editable = editable
        p.readable = readable
        p.field = '{}.{}'.format(sf_obj, field)
        return p

    def add_object_permissions_to_profile(self, sf_obj, profile, allow_create=False, allow_read=False, allow_edit=False, allow_delete=False,
                                 modify_all=False, view_all=False):
        Profile = self._md_api.get_type('Profile')
        p = Profile()
        p.fullName = profile
        perm = self.create_object_permission(sf_obj, allow_create=allow_create, allow_read=allow_read, allow_edit=allow_edit, allow_delete=allow_delete,
                                 modify_all=modify_all, view_all=view_all)
        p.objectPermissions = [perm]
        self._md_api.update_metadata(p)

    def create_object_permission(self, sf_obj, allow_create=False, allow_read=False, allow_edit=False, allow_delete=False,
                                 modify_all=False, view_all=False):
        ProfileObjectPermissions = self._md_api.get_type('ProfileObjectPermissions')
        perm = ProfileObjectPermissions()
        perm.object = sf_obj
        perm.allowCreate = allow_create
        perm.allowRead = allow_read
        perm.allowEdit = allow_edit
        perm.allowDelete = allow_delete
        perm.modifyAllRecords = modify_all
        perm.viewAllRecords = view_all
        return perm

    def create_permission_set(self, name, label):
        PermissionSet = self._md_api.get_type('PermissionSet')
        p = PermissionSet()
        p.fullName = name
        p.label = label
        return p

    def replace_attachments_with_files_and_notes_on_layout(self, layout_name, namespace_prefix=None):
        RelatedListItem = self._md_api.get_type('RelatedListItem')
        split = layout_name.split('-', 1)
        ATTACHMENT_RELATED_LIST_NAMES = ['RelatedNoteList', 'RelatedActivityAttachmentList']

        layout_name = '{}-{}__{}'.format(split[0], namespace_prefix, split[1]) if namespace_prefix else layout_name
        layout = self._md_api.read_metadata('Layout', layout_name)[0]
        attachmentRelatedList = [i for i in layout.relatedLists if i.relatedList and i.relatedList in ATTACHMENT_RELATED_LIST_NAMES]
        if attachmentRelatedList:
            print("Found attachments on {}. Attempting to remove.".format(layout_name))
            relatedLists = [i for i in layout.relatedLists if i.relatedList and not i.relatedList in ATTACHMENT_RELATED_LIST_NAMES ]

            files = RelatedListItem()
            files.relatedList = 'RelatedFileList'
            relatedLists.append(files)

            notes = RelatedListItem()
            notes.relatedList = 'RelatedContentNoteList'
            relatedLists.append(notes)

            layout.relatedLists = relatedLists

        self._md_api.update_metadata(layout)

    def get_layouts_for_object(self, sf_obj):
        layouts = self.list_metadata('Layout')
        return [x for x in layouts if sf_obj + '-' in x.fullName]

    def replace_attachments_with_files_and_notes_on_object(self, sf_obj):
        layouts = self.get_layouts_for_object(sf_obj)
        for l in layouts:
            self.replace_attachments_with_files_and_notes_on_layout(l.fullName, l.namespacePrefix)

        #layout[0].relatedLists = [i for i in relatedListItems if i.relatedList != 'RelatedNoteList']
        # RelatedNoteListlayou

class InvalidFieldType(Exception):
    pass
