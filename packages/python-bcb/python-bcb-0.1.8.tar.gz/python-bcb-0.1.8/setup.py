# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bcb']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0',
 'lxml>=4.9.1,<5.0.0',
 'pandas>=1.4.4,<2.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'python-bcb',
    'version': '0.1.8',
    'description': '',
    'long_description': '# python-bcb\n\n**python-bcb** é uma interface em Python estruturada para obter informações\nda API de dados abertos do [Banco Central do Brasil](https://www.bcb.gov.br).\n\n[![Downloads](https://img.shields.io/pypi/dm/python-bcb.svg)](https://pypi.python.org/pypi/python-bcb/)\n[![image](https://img.shields.io/pypi/v/python-bcb.svg?color=green)](https://pypi.python.org/pypi/python-bcb/)\n![Sphinx workflow](https://github.com/wilsonfreitas/python-bcb/actions/workflows/sphinx.yml/badge.svg)\n\n\nO projeto de [Dados Abertos do Banco Central do Brasil](https://dadosabertos.bcb.gov.br/)\ndisponibiliza diversas APIs provendo acesso direto a dados de:\n\n* Moedas\n* Taxas de Juros\n* Índices de preços\n* Informações de Instituições Financeiras\n* Expectativas do Mercado (Expectativas do Boletim FOCUS)\n* E muito outros ...\n\n# Instalação\n\n**python-bcb** está disponível no [Python Package Index](https://pypi.org/project/python-bcb/) e pode ser instalado via `pip` usando.\n\n```shell\npip install python-bcb\n```\n\n# APIs\n\n\n## SGS\nUtiliza o webservice do SGS\n(`Sistema Gerenciador de Séries Temporais <https://www3.bcb.gov.br/sgspub/>`_)\npara obter os dados.\n\n## Conversor de Moedas\n\nImplementado no módulo `currency`, um conjunto de funções que realiza webscraping\nno site do [Conversos de Moedas](https://www.bcb.gov.br/conversao)\ndo Banco Central, possível obter séries temporais de frequência diária\nde diversas moedas.\n\n## Moedas OData\n\nO Banco Central disponibiliza diversas informações em APIs que\nseguem o padrão [OData](https://odata.org).\nA classe `bcb.PTAX` implementa uma API OData que\nentrega os boletins diários de taxas de câmbio do Banco Central.\nEsta API entrega mais informações do que o que é obtido no\n`Conversor de Moedas`.\n\n## Expectativas\n\nA API de Expectativas de Mercado traz todas as estatísticas das variáveis\nmacroeconômicas fornecidos por um conjuto de instituições do mercado\nfinanceiro.\nA classe `bcb.Expectativas` implementa essa interface no\npadrão OData.\n',
    'author': 'wilsonfreitas',
    'author_email': 'wilson.freitas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
