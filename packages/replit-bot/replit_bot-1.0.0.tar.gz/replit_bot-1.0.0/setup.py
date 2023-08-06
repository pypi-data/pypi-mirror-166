# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['replit_bot',
 'replit_bot.replit_bot',
 'replit_bot.replit_bot.utils',
 'replit_bot.tests']

package_data = \
{'': ['*'], 'replit_bot.replit_bot': ['templates/*']}

install_requires = \
['Flask>=2.2.0,<3.0.0',
 'datauri>=1.0.0,<2.0.0',
 'replit>=3.2.4,<4.0.0',
 'requests>=2.28.1,<3.0.0',
 'waitress>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'replit-bot',
    'version': '1.0.0',
    'description': "create a replit bot using an API endpoint similar to discord. Includes [replapi-it](https://replit.com/@PikachuB2005/replapi-it) (3.20, made by @pikachub2005) python implementation. most up to date python version of replapi-it not fully tested. working on @replit/crosis.py. automatically creates a command docs. queries are at the moment whitelisted so only people with whitelisted sid's can use it. basic python implementation of a node event listener. Known bugs: notification query does not return the username of author",
    'long_description': '# working on it',
    'author': 'bigminiboss',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://replit.com/@bigminiboss/repbot?v=1',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.9',
}


setup(**setup_kwargs)
