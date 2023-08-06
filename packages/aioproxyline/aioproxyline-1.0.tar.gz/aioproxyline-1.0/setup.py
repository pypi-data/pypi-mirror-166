# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioproxyline',
 'aioproxyline.core',
 'aioproxyline.core.abc',
 'aioproxyline.core.methods',
 'aioproxyline.exceptions',
 'aioproxyline.types']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'aioproxyline',
    'version': '1.0',
    'description': 'Asynchronous wrapper to interact with proxyline.net API',
    'long_description': None,
    'author': 'Marple',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
