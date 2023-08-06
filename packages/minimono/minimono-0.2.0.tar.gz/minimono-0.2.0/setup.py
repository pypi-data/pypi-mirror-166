# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minimono', 'minimono.API']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.1,<2.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'minimono',
    'version': '0.2.0',
    'description': 'A wrapper for monobanks API. With caching and serialization.',
    'long_description': None,
    'author': 'Arthur Ryzhak',
    'author_email': 'ryzhakar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
