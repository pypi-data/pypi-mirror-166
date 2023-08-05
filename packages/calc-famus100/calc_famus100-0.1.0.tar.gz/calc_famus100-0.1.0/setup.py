# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['calc_famus100']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'calc-famus100',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'famus99',
    'author_email': '73717006+famus99@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
