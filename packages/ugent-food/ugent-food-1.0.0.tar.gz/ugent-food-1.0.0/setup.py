# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ugent_food', 'ugent_food.api', 'ugent_food.cli', 'ugent_food.exceptions']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'click>=8.1.3,<9.0.0',
 'dacite>=1.6.0,<2.0.0',
 'tabulate>=0.8.10,<0.9.0']

setup_kwargs = {
    'name': 'ugent-food',
    'version': '1.0.0',
    'description': 'Command-line tool to get the current menu for Ghent University restaurants',
    'long_description': 'None',
    'author': 'stijndcl',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
