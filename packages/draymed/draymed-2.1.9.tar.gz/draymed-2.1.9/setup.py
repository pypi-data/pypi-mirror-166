# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['draymed', 'draymed.codes']

package_data = \
{'': ['*'], 'draymed': ['data/*']}

setup_kwargs = {
    'name': 'draymed',
    'version': '2.1.9',
    'description': 'Draymed library for SNOMED codes and more',
    'long_description': None,
    'author': 'Adam Romano',
    'author_email': 'adam.romano@sensynehealth.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/polaris-foundation/draymed',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
