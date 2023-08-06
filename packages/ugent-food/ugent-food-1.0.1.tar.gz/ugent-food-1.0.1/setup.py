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

entry_points = \
{'console_scripts': ['ugent-food = ugent_food:main']}

setup_kwargs = {
    'name': 'ugent-food',
    'version': '1.0.1',
    'description': 'Command-line tool to get the current menu for Ghent University restaurants',
    'long_description': '# ugent-food\n\n![PyPI](https://img.shields.io/pypi/v/ugent_food)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ugent_food)\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/stijndcl/ugent-food/Python)\n\nCommand-line tool to get the current menu for Ghent University restaurants.\n\nThis application was made using [Zeus WPI](https://github.com/ZeusWPI)\'\ns [Hydra API](https://github.com/ZeusWPI/hydra/blob/master/api-resto-02.md).\n\n## Installation\n\nIt\'s recommended to install the tool using [``pipx``](https://pypa.github.io/pipx/#install-pipx) to allow running the\ncommand from anywhere on your PC, without having to invoke it using `python3 -m ugent_food`.\n\n```sh\n$ pipx install ugent-food\n```\n\nIf you don\'t want to use `pipx`, it can also be installed using `pip`:\n\n```sh\n$ pip3 install --user ugent-food\n```\n\n_Note: **Don\'t install this in a Virtual Environment**, as you won\'t be able to run it from anywhere else._\n\nNext, you can add an alias to your `.bashrc` or `.zshrc` for your own convenience:\n\n```sh\n# If you installed using pipx\n$ echo \'alias food="ugent-food"\' >> ~/.bashrc\n$ echo \'alias food="ugent-food"\' >> ~/.zshrc\n\n# If you installed using pip\n$ echo \'alias food="python3 -m ugent_food"\' >> ~/.bashrc\n$ echo \'alias food="python3 -m ugent_food"\' >> ~/.zshrc\n```\n\nYou can now simply use `food` to run the tool.\n\n## Usage\n\n_To keep the examples short, they use `food` instead of `python3 -m ugent_food` to invoke the tool._\n\n### Menus\n\nTo get the menu for a given day, use the ``menu`` command. By default, not passing any arguments will fetch today\'s\nmenu:\n\n```sh\n$ food\n```\n\nFor convenience, passing this command is **optional**. You can immediately pass a day (or subcommand) instead of having\nto explicitly add this as well. The above line is equivalent to\n\n```sh\n$ food menu\n```\n\n#### Arguments\n\nTo fetch the menu for a specific day, an extra argument can be passed. This can either be a weekday, an offset (relative\nto today), or a day in `DD/MM`-format:\n\n```sh\n$ food monday\n$ food tomorrow\n$ food 21/09\n```\n\n### Configuration\n\nThe tool has a couple of settings that you can configure using the `set` subcommand:\n\n```sh\n$ food config set skip_weekends true\n```\n\nYou can list the current settings with `config ls`:\n\n```sh\n$ food config ls\n```\n\n#### Available settings\n\nNote that `boolean` arguments can be supplied as any of `[true, false, t, f, 1, 0]`.\n\n| Name          | Description                                                                                                                                                                                                                        | Type (choices)                                                 | Default |\n|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------|---------|\n| hidden        | A list of meal kinds that should be hidden when fetching menus. This can be useful for vegetarians and vegans who don\'t care about the meat dishes.                                                                                | List\\[String\\] ("fish", "meat", "soup", "vegan", "vegetarian") | []      |\n| language      | The language used to fetch the menus in.                                                                                                                                                                                           | String ("en" 🇬🇧 , "nl" 🇧🇪/🇳🇱)                            | "en"    |\n| skip_weekends | Whether to automatically skip weekends when fetching menus. This defaults to true because the restaurants aren\'t usually open during weekends. For example: using the tool on a Saturday will show the menu for the coming Monday. | Boolean                                                        | True    |\n',
    'author': 'stijndcl',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stijndcl/ugent-food',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
