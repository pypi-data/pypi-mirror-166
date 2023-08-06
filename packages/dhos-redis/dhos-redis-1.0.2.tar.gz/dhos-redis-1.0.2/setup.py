# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dhosredis']

package_data = \
{'': ['*']}

install_requires = \
['environs>=9.0.0,<10.0.0', 'redis>=3.0.0,<4.0.0', 'she-logging>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'dhos-redis',
    'version': '1.0.2',
    'description': 'Redis functionality for Polaris',
    'long_description': None,
    'author': 'Jon Daly',
    'author_email': 'jonathan.daly@sensynehealth.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/polaris-foundation/dhos-redis',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
