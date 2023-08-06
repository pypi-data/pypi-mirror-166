# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['auth0_api_client', 'auth0_api_client.models']

package_data = \
{'': ['*']}

install_requires = \
['environs>=9.0.0,<10.0.0',
 'requests>=2.0.0,<3.0.0',
 'she-logging>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'auth0-api-client',
    'version': '1.3.6',
    'description': 'Client library for Auth0 management API',
    'long_description': None,
    'author': 'Jon Daly',
    'author_email': 'jonathan.daly@sensynehealth.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/polaris-foundation/auth0-api-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
