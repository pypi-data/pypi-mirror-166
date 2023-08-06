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
    'version': '0.1.2',
    'description': 'Asynchronous functions for making HTTP requests to Gancio istances',
    'long_description': '# gancio_requests\n`gancio_requests` is a tool for making asynchronous HTTP \nrequests to the API of a specified Gancio instance. [Gancio](https://gancio.org/) is a shared \nagenda for local communities, a project which wants to provide \na self-hosted solution to host and organize events.  \n\nThis repo aims to supply a convenient set of functions to fetch\ndata from a gancio instance (e.g. scheduled events, the image or\ndescription of an event).\n\n## Installation\nTo install the latest version of the library just download \n(or clone) the current project, open a terminal and run the \nfollowing commands:\n\n```\npip install -r requirements.txt\npip install .\n```\n\nAlternatively use pip\n\n```python\npip install gancio_requests\n```\n\n### Dependencies\nAt the moment I have tested the library only on _python == 3.10.4_  \n\nThe library requires the dependencies specified in _requirements.txt_\nand I haven\'t still tested other versions.\n\n## Usage\n\n### Command line interface\n\n```\npython3 -m gancio_requests [-h] gancio_instance\n```\n_gancio_instance_ is the URL of the instance from which we want\nto fetch the data.  \n\nThe output displays the list of events starting of 00:00:00 of\nthe current day. The information about an event is shown this \nway:\n```\nEVENT_NAME\n[STARTING_TIME | END_TIME]\nPLACE_NAME - ADDRESS\nLIST_OF_TAGS (optional)\nEVENT_URL\n```\n#### Example\n\n##### Input\n```\npython3 -m gancio_requests https://gancio.cisti.org\n```\n\n##### Output\n```\nCrazy toga party\n[2022-08-11 22:30:00 | 2022-08-12 00:00:00]\nColosseo - Piazza del Colosseo, Roma\nTags: ["colosseum", "ancient rome", "toga party"]\nhttps://gancio.cisti.org/crazy-toga-party\n\nGioco del ponte\n[2022-09-10 22:00:00 | 2022-09-10 23:00:00]\nPonte di mezzo - Ponte di Mezzo, 1, 56125 Pisa\nhttps://gancio.cisti.org/gioco-del-ponte\n```\n\n### Python library\nAfter the installation, it is possible to use the package\ndirectly from the python interpreter by using \n`import gancio_requests`.\n\n### Caching\n\nIt is possible to cache HTTP requests thanks to \n[aiohttp-client-cache](https://aiohttp-client-cache.readthedocs.io/en/latest/).\nAll the functions shown above have an optional parameter \ncalled _cache_ which accepts a [_aiohttp_client_cache.backends_](https://aiohttp-client-cache.readthedocs.io/en/latest/backends.html)\nobject.\n```\nimport asyncio\nfrom aiohttp_client_cache import SQLiteBackend\nfrom gancio_requests.request import get_events\n\nurl = \'https://gancio.cisti.org\'\nparams = {"start": 0}\ncache = SQLiteBackend(\n    cache_name = "Test.db"\n)\nresult = asyncio.run(get_events(url, params, cache=cache)) \n```\n',
    'author': 'Gianluca Morcaldi',
    'author_email': 'bendico765@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bendico765/gancio_requests',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
