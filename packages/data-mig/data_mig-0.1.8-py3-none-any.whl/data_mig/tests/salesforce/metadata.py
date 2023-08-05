from data_mig.salesforce.metadata import MetadataWrapper
from data_mig.salesforce.oauth import SalesforceAuth
from data_mig.utils.config import Config

cfg = Config(path='../../../')
mdw = MetadataWrapper(cfg)

def metadata_test():
    mdw = MetadataWrapper(cfg)
    mdw.create_external_id_field('Account')
    mdw.create_import_tag_field('Account')
    mdw.add_field_permissions_to_profile('Account', 'Import_Tag__c', 'Admin')
    mdw.add_field_permissions_to_profile('Account', 'External_Import_Id__c', 'Admin')
    mdw.add_field_to_all_layouts('Account', 'Import_Tag__c')
    mdw.add_field_to_all_layouts('Account', 'External_Import_Id__c')


# s.add_field_permissions_to_profile('Opportunity', 'Expected_Demographics__c', 'Fundraising and Development')


def add_all_custom_fields_to_custom_profiles():
    fields_to_add = get_fields_to_add('NamespacePrefix = \'stayclassy\'')
    add_fields_to_profiles(fields_to_add)


def get_fields(filter):
    if filter:
        filter = ' WHERE {}'.format(filter)
    all_fields = mdw._md_api.tooling_service.query("""SELECT Id, DeveloperName, NamespacePrefix, RelationshipLabel, ManageableState, EntityDefinition.QualifiedApiName
                                                        FROM CustomField{}
                                                        """.format(filter))

    fields_to_add = []
    for i in all_fields.body.result.records:
        # print('{}.{}'.format(i.EntityDefinition.QualifiedApiName, i.DeveloperName))
        field = mdw._md_api.tooling_service.query(
            'SELECT Id, DeveloperName, NamespacePrefix, RelationshipLabel, ManageableState, MetaData, FullName, EntityDefinition.QualifiedApiName FROM CustomField WHERE Id = \'{}\''.format(
                i.Id)).body.result.records[0]
        objectandfieldname = field.FullName.split('.')
        print('Preparing to add {}'.format(field.FullName))
        print('Required {}'.format(field.Metadata.required))
        objectname = objectandfieldname[0]
        fieldname = objectandfieldname[1]
        required = field.Metadata.required
 #       if field.Metadata.required != False or objectname in ['stayclassy__Classy_API_Settings__c', 'stayclassy__Classy_Configuration__c', 'stayclassy__Classy_Contact_Matching__c']:
 #           print('Skipping field: {}'.format(field.FullName))
 #           continue

        fields_to_add.append({'object': objectname, 'field': fieldname, 'required': required})
#        print(mdw.add_field_permissions_to_permission_set(object, field, 'Permissions_for_Classy', 'Permissions for Classy'))

    return fields_to_add

#Permissions for Classy

def add_fields_to_profiles(fields_to_add):
    mdw.add_fields_to_profile(fields_to_add, 'US - Classy/Advocacy')
    #mdw.add_fields_to_profile(fields_to_add, 'US - System Administrator')
    #mdw.add_fields_to_profile(fields_to_add, 'System Administrator')
    mdw.add_fields_to_permission_set(fields_to_add, 'Permissions_for_Classy', 'Permissions for Classy')
    #   mdw.add_field_permissions_to_profile(objectname, fieldname, 'US - Advocacy Staff')
    #   mdw.add_field_permissions_to_profile(objectname, fieldname, 'US - System Administrator')
    #   mdw.add_field_permissions_to_profile(objectname, fieldname, 'System Administrator')


def add_all_custom_objects_to_custom_profiles():
    for obj in ['npsp__Account_Soft_Credit__c', 'npsp__Grant_Deadline__c', 'Grantee_Form__c',
                'Metric_Demographic__c', ]:
        for profile in ['Fundraising and Development', 'Program Staff', 'Executive Management']:
            mdw.add_object_permissions_to_profile(obj, profile, allow_create=True, allow_read=True, allow_edit=True,
                                                  allow_delete=True)


if __name__ == '__main__':
    #add_all_custom_objects_to_custom_profiles()
    pass

def get_valid_field_types():
    import xml.etree.ElementTree as ET
    tree = ET.fromstring(mdw._md_api.metadata_wsdl)
    types_xml = [c for c in tree if 'types' in c.tag][0][0]
    values_xml = [c[0] for c in types_xml if c.attrib.get('name') == 'FieldType'][0]
    values = [x.attrib['value'] for x in values_xml]
    return values


# obj='Opportunity'
# profile = 'Program Staff'
# s.add_object_permissions_to_profile(obj, profile, allow_create=True, allow_read=True, allow_edit=True, allow_delete=True)