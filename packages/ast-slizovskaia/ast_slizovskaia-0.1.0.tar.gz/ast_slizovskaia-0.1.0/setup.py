# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ast_slizovskaia']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ast-slizovskaia',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Olga Slizovskaia',
    'author_email': 'oslizovskaia@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
