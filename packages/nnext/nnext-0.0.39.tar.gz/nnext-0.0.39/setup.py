# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nnext',
 'nnext.conversions',
 'nnext.grpc',
 'nnext.http',
 'nnext.http.api',
 'nnext.http.models',
 'nnext.uploader']

package_data = \
{'': ['*']}

install_requires = \
['betterproto==2.0.0b4',
 'grpcio>=1.46.0,<2.0.0',
 'httpx[http2]>=0.23.0,<0.24.0',
 'loguru>=0.5.3,<0.6.0',
 'nest-asyncio>=1.5.5,<2.0.0',
 'numpy>=1.21,<2.0',
 'pydantic>=1.8,<2.0',
 'tqdm>=4.56.0,<5.0.0',
 'typing-extensions>=4.0.0,<5.0.0']

setup_kwargs = {
    'name': 'nnext',
    'version': '0.0.39',
    'description': 'Client library for the NNext vector search engine',
    'long_description': '\n# <a href="https://nnext.ai/"><img src="https://d135j1zm1liera.cloudfront.net/nnext-logo-wide.png" height="100" alt="Apollo Client"></a>\n\n## About\n\nThis repository houses the source code for the python client associated with NNext.\n\nNNext is a\n* ⚡ blazingly fast\n* 🔍 nearest-neighbors vector search engine\n\n<a href="https://tiny.one/nnext-slk-comm-gh"><img src="https://img.shields.io/badge/chat-slack-orange.svg?logo=slack&style=flat"></a>\n<a href="https://twitter.com/intent/follow?screen_name=nnextai"><img src="https://img.shields.io/badge/Follow-nnextai-blue.svg?style=flat&logo=twitter"></a>\n\n[Installation](#installation) |  [Quick Start](#quick-start) | [Documentation](#documentation)\n\n## Installation\nTo install the pynnext client, activate a virtual environment, and install via pip:\n\n```zsh\npip install nnext\n```\n\n## Quick Start\n\nHere\'s a quick example showcasing how you can create an index, insert vectors/documents and search among them via NNext.\n\nLet\'s begin by installing the NNext server.\n\n```zsh\ndocker run -p 6040:6040 -p 6041:6041 \\\n\t-v ~/.nnext/data:/.nnext/data \\\n\tnnext/nnext\n```\n\n## Documentation\nMore documentation is available here:\n\nhttps://nnext.ai/docs',
    'author': 'NNext Team',
    'author_email': 'pynnext@nnext.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nnextdb/pynnext',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
