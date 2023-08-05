from faker import Faker
from ..sql.tools import SQLTools
from ..utils.config import Config
import pandas as pd


def fakePeople():
    fake = Faker()
    fakes = []
    headers = ['FirstName', 'LastName', 'MailingStreet', 'MailingCity', 'MailingState', 'MailingPostalCode', 'Email', 'Phone', 'Contact_Id__c']
    for i in range(500):
        state = fake.state_abbr()
        f = [fake.first_name(), fake.last_name(), fake.street_address(), fake.city(), state, fake.postcode_in_state(state), fake.email(), fake.phone_number(), i]
        fakes.append(f)
    df = pd.DataFrame(fakes, columns=headers)
    cfg = Config()
    sql_con = SQLTools(cfg).sqlalchemy_connect_to_db()
    df.to_sql('People', sql_con, if_exists='replace', index=False)
    return df

