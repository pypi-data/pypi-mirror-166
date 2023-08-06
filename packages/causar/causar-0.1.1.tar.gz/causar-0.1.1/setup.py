# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['causar', 'causar.transactions']

package_data = \
{'': ['*']}

install_requires = \
['disnake>=2.5.2,<3.0.0']

setup_kwargs = {
    'name': 'causar',
    'version': '0.1.1',
    'description': 'A high level testing framework for Disnake bots',
    'long_description': "Causar\n---\n\n### A high level testing framework for Disnake bots\n\nWritten for my needs, open source for yours.\n\n---\n\nCurrently still in extremely early development so don't expect a lot.",
    'author': 'Skelmis',
    'author_email': 'ethan@koldfusion.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Skelmis/Causar',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
