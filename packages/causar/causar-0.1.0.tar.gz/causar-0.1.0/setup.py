# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['causar']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'causar',
    'version': '0.1.0',
    'description': 'A high level testing framework for Disnake bots',
    'long_description': None,
    'author': 'Skelmis',
    'author_email': 'ethan@koldfusion.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
