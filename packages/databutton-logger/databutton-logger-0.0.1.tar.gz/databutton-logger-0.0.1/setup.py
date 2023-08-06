# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logger']

package_data = \
{'': ['*']}

install_requires = \
['asgi-correlation-id>=3.0.1,<4.0.0',
 'fastapi>=0.82.0,<0.83.0',
 'loguru>=0.6.0,<0.7.0',
 'uvicorn>=0.18.3,<0.19.0']

setup_kwargs = {
    'name': 'databutton-logger',
    'version': '0.0.1',
    'description': 'Logger utilities for databutton',
    'long_description': None,
    'author': 'Databutton',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
