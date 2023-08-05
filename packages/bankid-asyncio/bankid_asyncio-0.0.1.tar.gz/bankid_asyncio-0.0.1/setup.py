# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bankid_asyncio', 'bankid_asyncio.clients']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.81.0,<0.82.0', 'httpx>=0.23.0,<0.24.0', 'pydantic>=1.9.2,<2.0.0']

setup_kwargs = {
    'name': 'bankid-asyncio',
    'version': '0.0.1',
    'description': 'BankID client for Python with asyncio support.',
    'long_description': '# bankid_asyncio\nBankID client for Python with asyncio support.\n\n![GitHub](https://img.shields.io/github/license/Kostiantyn-Salnykov/bankid_asyncio)\n![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/Kostiantyn-Salnykov/bankid_asyncio/Python%20package/main)\n![GitHub last commit (branch)](https://img.shields.io/github/last-commit/Kostiantyn-Salnykov/bankid_asyncio/main)\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/bankid-asyncio)\n![PyPI](https://img.shields.io/pypi/v/bankid-asyncio)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/bankid-asyncio)\n\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n[![](https://img.shields.io/badge/code%20style-black-000000?style=flat)](https://github.com/psf/black)\n',
    'author': 'Kostiantyn Salnykov',
    'author_email': 'kostiantyn.salnykov@gmail.com',
    'maintainer': 'Kostiantyn Salnykov',
    'maintainer_email': 'kostiantyn.salnykov@gmail.com',
    'url': 'https://github.com/Kostiantyn-Salnykov/bankid_asyncio/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
