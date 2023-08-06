# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ast_slizovskaia']

package_data = \
{'': ['*']}

install_requires = \
['einops>=0.4.1,<0.5.0',
 'librosa>=0.9.2,<0.10.0',
 'numpy>=1.21.0,<2.0.0',
 'pandas>=1.4.4,<2.0.0',
 'pytorch-lightning>=1.3.8,<2.0.0',
 'torchaudio>=0.12.1,<0.13.0',
 'tqdm>=4.61.2,<5.0.0']

setup_kwargs = {
    'name': 'ast-slizovskaia',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'Olga Slizovskaia',
    'author_email': 'oslizovskaia@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
