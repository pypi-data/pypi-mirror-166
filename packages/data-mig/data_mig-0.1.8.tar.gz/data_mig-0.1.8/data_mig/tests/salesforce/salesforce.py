import data_mig.utils.config as cf
from data_mig.salesforce.oauth import *
from data_mig.utils.exceptions import TranslationException
from data_mig.salesforce.loader import SalesforceDataLoader
import strgen as SG
import pandas as pd
import numpy as np

cfg = cf.Config(path='../../')

def test_authorize():
    auth = SalesforceAuth(cfg)
    token = auth.get_token()
    if not token:
        print('ERROR: Failed to get token!')
    else:
        print('Got Token!')

def dummy_data():
    strings = []
    for i in range(50):
        strings.append(SG.StringGenerator('[\w]{1:15}').render())

    lists = []
    for i in range(60000):
        lists.append(np.random.choice(strings, 4))

    return lists

def test_load_data():
    df_sf = pd.DataFrame(dummy_data(), columns=['LastName', 'FirstName', 'MailingStreet', 'Email'])
    params = {
        'sf_object': 'contact',
        'operation': 'insert',
    }

    st.load_dataframe(df_sf, params)

def test_check_filtering():

    df_sf = pd.DataFrame(dummy_data(), columns=['FirstName', 'MailingStreet', 'Email', 'MailingState'])

    st = SalesforceDataLoader(cfg)

    print('TEST: Check for missing required fields')
    try:
        st.check_schema(df_sf, 'contact')
    except ValidationException as e:
        assert e.message == 'Required field(s) (LastName) not found.', 'Required Field Missing Not Caught!!! {}'.format(e.message)

    print('TEST: Check for invalid column names')

    df_sf_invalid_colnames = pd.DataFrame(dummy_data(), columns=['FirstName', 'LastName', 'Email', 'Test'])

    try:
        st.check_schema(df_sf_invalid_colnames, 'contact')
    except ValidationException as e:
        assert e.message == 'Invalid column(s) found: (Test)', 'Invalid Column Test not Detected'

    print('TEST: Filtering Garbage Emails')

    df_sf_emails_and_booleans = dummy_data_test_cleanup()

    st.check_schema(df_sf_emails_and_booleans, 'contact', filter_invalid=True)
    email_field_values = np.array(df_sf_emails_and_booleans['HasOptedOutOfEmail'].unique())
    valid_email_field_values = np.array([0, 1])
    assert np.array_equal(email_field_values.sort(), valid_email_field_values.sort()), 'Only Valid Boolean Should Remain'


def dummy_data_test_cleanup():
    bool_strings = ['1', 1, 0, True, False, 'TRUE', 'FALSE', 'X', 'Y', 'N']
    email_strings = ['test@test.com', 'me@gmail.com', 'bademail.']
    words = []
    for i in range(50):
        words.append(SG.StringGenerator('[\w]{5:15}').render())

    lists = []
    for i in range(500):
        l = np.random.choice(words, 3)
        l = np.append(l, np.random.choice(email_strings, 1, p=[0.85, 0.10, 0.05]))
        l = np.append(l, np.random.choice(bool_strings, 1))
        lists.append(l)

    df_sf = pd.DataFrame(lists, columns=['FirstName', 'LastName', 'MailingState', 'Email', 'HasOptedOutOfEmail'])

    return df_sf

if __name__ == '__main__':
    test_authorize()
    test_check_filtering()


