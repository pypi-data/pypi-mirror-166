# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['htmlatex']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0']

setup_kwargs = {
    'name': 'htmlatex',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Linus',
    'author_email': 'linuskmr.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
