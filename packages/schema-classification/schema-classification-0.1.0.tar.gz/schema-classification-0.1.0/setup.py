# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['schema_classification']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'schema-classification',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Craig Trim',
    'author_email': 'craigtrim@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '==3.8.5',
}


setup(**setup_kwargs)
