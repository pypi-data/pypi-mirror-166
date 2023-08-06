# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['entity_classification',
 'entity_classification.bp',
 'entity_classification.dmo',
 'entity_classification.svc']

package_data = \
{'': ['*']}

install_requires = \
['baseblock']

setup_kwargs = {
    'name': 'entity-classification',
    'version': '0.1.1',
    'description': 'Perform Intent Classification using a list of Entities',
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
