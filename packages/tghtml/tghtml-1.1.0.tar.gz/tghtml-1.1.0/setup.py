# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tghtml']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0', 'readability-lxml>=0.8.1,<0.9.0']

setup_kwargs = {
    'name': 'tghtml',
    'version': '1.1.0',
    'description': 'Simple tool for parse common HTML to Telegram HTML',
    'long_description': None,
    'author': 'Daniel Zakharov',
    'author_email': 'gzdan734@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
