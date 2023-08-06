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
    'version': '0.1.1',
    'description': 'Informações da Cidade pelo IBGE ou TOM',
    'long_description': "# cidade_ibge_tom\n[![PyPI](https://img.shields.io/pypi/v/cidade_ibge_tom)](https://pypi.org/project/cidade_ibge_tom/) ![pyversions](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue) ![https://github.com/leogregianin/cidade_ibge_tom/actions](https://github.com/leogregianin/cidade_ibge_tom/workflows/CI/badge.svg?branch=main)\n\n\n## Cidade IBGE TOM\n\nDemonstra informações da Cidade pelo código IBGE ou pelo código TOM.\n\n`Código IBGE` é um padrão de código das Cidades brasileiras, que é composto por 7 dígitos, sendo os 2 primeiros o código do Estado.\n\n`Código TOM` é um padrão de código das Cidades brasileiras utilizado por sistemas, por exemplo, [SIAFI](https://siafi.tesouro.gov.br/) - Sistema Integrado de Administração Financeira do Governo Federal, que é composto por 4 dígitos. A tabela completa dos códigos pode ser obtida [aqui](https://www.tesourotransparente.gov.br/ckan/dataset/lista-de-municipios-do-siafi/resource/eebb3bc6-9eea-4496-8bcf-304f33155282).\n\nNeste pacote python temos o código IBGE, código TOM e o nome da Cidade relacionado.\n\n## Instalação\n\n```bash\npip install cidade_ibge_tom\n```\n\n## Utilização\n\n* Informando o código IBGE 5300108:\n```python\nfrom cidade_ibge_tom import info_cidade\n\nprint(info_cidade(codigo='5300108'))\n{'ibge': '5300108', 'tom': '9701', 'nome': 'Brasília-DF'}\n```\n\n* Informando o código TOM 7107:\n```python\nfrom cidade_ibge_tom import info_cidade\n\nprint(info_cidade(codigo='7107'))\n{'ibge': '3550308', 'tom': '7107', 'nome': 'São Paulo-SP'}\n```\n\n## Licença\n\n  MIT License",
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
