# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['algerography', 'algerography.management.commands', 'algerography.migrations']

package_data = \
{'': ['*'], 'algerography': ['fixtures/*']}

setup_kwargs = {
    'name': 'algerography',
    'version': '0.2.1',
    'description': '',
    'long_description': None,
    'author': 'fathibensari',
    'author_email': 'fethibensari@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
