# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cidade_ibge_tom']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=5.0.4,<6.0.0',
 'mypy>=0.971,<0.972',
 'pytest-cov>=3.0.0,<4.0.0',
 'pytest>=7.1.3,<8.0.0']

setup_kwargs = {
    'name': 'cidade-ibge-tom',
    'version': '0.1.0',
    'description': 'Informações da Cidade pelo IBGE ou TOM',
    'long_description': None,
    'author': 'Leonardo Gregianin',
    'author_email': 'leogregianin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
