# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_mig',
 'data_mig.csvtools',
 'data_mig.jobs',
 'data_mig.salesforce',
 'data_mig.salesforce.wsdl',
 'data_mig.sql',
 'data_mig.tests',
 'data_mig.tests.jobs',
 'data_mig.tests.salesforce',
 'data_mig.tests.sql',
 'data_mig.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'SQLAlchemy>=1.4.39,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'progressbar2>=4.0.0,<5.0.0',
 'pyodbc>=4.0.34,<5.0.0',
 'pyotp>=2.6.0,<3.0.0',
 'pytest-mock>=3.8.2,<4.0.0',
 'pytest>=7.1.2,<8.0.0',
 'requests>=2.28.1,<3.0.0',
 'simple-salesforce>=1.12.1,<2.0.0',
 'simplejson>=3.17.6,<4.0.0',
 'sqlparse>=0.4.2,<0.5.0',
 'validate_email>=1.3,<2.0',
 'xlrd>=2.0.1,<3.0.0',
 'zeep>=4.1.0,<5.0.0']

setup_kwargs = {
    'name': 'data-mig',
    'version': '0.1.8',
    'description': 'Arroyo: The Fíonta Data Migration Toolkit',
    'long_description': None,
    'author': 'David Manuel',
    'author_email': 'dmanuel@fionta.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
