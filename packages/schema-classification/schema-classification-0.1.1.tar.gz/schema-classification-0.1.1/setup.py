# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['schema_classification',
 'schema_classification.bp',
 'schema_classification.dmo',
 'schema_classification.dto',
 'schema_classification.svc']

package_data = \
{'': ['*']}

install_requires = \
['baseblock']

setup_kwargs = {
    'name': 'schema-classification',
    'version': '0.1.1',
    'description': 'Perform Intent Classification using an External Schema',
    'long_description': None,
    'author': 'Craig Trim',
    'author_email': 'craigtrim@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.5',
}


setup(**setup_kwargs)
