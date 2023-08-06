# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gancio_telegram_bot',
 'gancio_telegram_bot.callbacks',
 'gancio_telegram_bot.handlers',
 'gancio_telegram_bot.utils',
 'gancio_telegram_bot.viz']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp-client-cache>=0.7.3,<0.8.0',
 'aiosqlite>=0.17.0,<0.18.0',
 'gancio-requests>=0.1.2,<0.2.0',
 'matplotlib>=3.5.3,<4.0.0',
 'pandas>=1.4.4,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'python-telegram-bot==20.0a4',
 'seaborn>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'gancio-telegram-bot',
    'version': '0.1.0',
    'description': 'A Telegram bot to interact with Gancio instances',
    'long_description': '# gancio_telegram_bot\n\n``gancio_telegram_bot`` is a bot which allows to interact with a specified Gancio instance.\n[Gancio](https://gancio.org/) is a shared agenda for local communities, a project which wants to provide\na self-hosted solution to host and organize events.  \n\n![screen-gif](./assets/bot_overview.gif)\n\n## Installation\nTo install the latest version of the bot just download (or clone) the current project,\nopen a terminal and run the following commands:\n```shell\npip install -r requirements.txt\npip install .\n```\n\nAlternatively, use pip:\n```shell\npip install gancio_telegram_bot\n```\n\nIt\'s also possible to create a docker image and run the application in a container; see [Docker usage](#docker). \n\n### Dependencies\nAt the moment I have tested the bot only on _python == 3.10.4_  \nThe bot requires the dependencies specified in _requirements.txt_ and I haven\'t still tested\nother versions.\n\n## Usage\n\n### Configuration file (.env)\n\nThe bot relies on environment variables for its configuration; some parameters are strictly required \n(e.g. AUTH_TOKEN, INSTANCE_URL), while others just allow to personalize the bot appearance.\n\n| Parameter                     | Function                                                                                             |\n|-------------------------------|------------------------------------------------------------------------------------------------------|\n| AUTH_TOKEN                    | Telegram bot authentication token                                                                    |\n| INSTANCE_URL                  | Url of the gancio instance from which fetch the events                                               |\n| SHOW_EVENT_URL                | Set to "True" if each event must be accompanied by its url on the Gancio instance (default is False) |\n| MENU_ELEMENTS                 | Number of events to show in a single message (default is 3)                                          |\n| CACHE_NAME                    | Path to the database used for caching (default disable the cache mechanism)                          |\n| HTTP_CACHE_EXPIRATION_SECONDS | How many seconds the cache lasts (default is 10 minutes)                                             |\n\n\n### Command line interface\n\n```shell\npython3 -m gancio_telegram_bot\n```\n\n### Docker\n\n```shell\ndocker compose up -d\n```\n\n## Visualisation\nThe package comes up with some functions to allow the parsing of the\nlogfile and the visualisation of statistics related to the usage of the bot.\n\n![](./assets/visualisation_example.png)\n\n## Todolist\n- Better define which versions of python and dependency packages are compatible.\n- Create some tests.\n- Allow to define more fine-grained queries for the events (e.g. display just the events in a specific date).\n- Make more visualisation plots.',
    'author': 'Gianluca Morcaldi',
    'author_email': 'bendico765@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bendico765/gancio_telegram_bot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
