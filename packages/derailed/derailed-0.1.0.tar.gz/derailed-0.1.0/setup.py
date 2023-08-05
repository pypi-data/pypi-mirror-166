# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['derailed', 'derailed.types']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'websockets>=10.3,<11.0']

setup_kwargs = {
    'name': 'derailed',
    'version': '0.1.0',
    'description': 'Python wrapper for the Derailed API',
    'long_description': None,
    'author': 'VincentRPS',
    'author_email': 'vincentbusiness55@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
