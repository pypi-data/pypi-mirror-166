# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gancio_requests']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp-client-cache>=0.7.3,<0.8.0',
 'aiohttp>=3.8.1,<4.0.0',
 'aiosignal>=1.2.0,<2.0.0',
 'beautifulsoup4>=4.11.1,<5.0.0']

setup_kwargs = {
    'name': 'gancio-requests',
    'version': '0.1.0',
    'description': 'Asynchronous functions for making HTTP requests to Gancio istances',
    'long_description': 'None',
    'author': 'Gianluca Morcaldi',
    'author_email': 'bendico765@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
