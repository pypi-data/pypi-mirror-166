# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['iterable', 'iterable.resources']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'iterable-api',
    'version': '0.1.3',
    'description': 'Iterable API wrapper',
    'long_description': "# Iterable API\n\nThis is a mostly complete wrapper of the Iterable API built with Python.\n\nThe interface is still in a state of flux, some methods will be renamed but the signatures should stay the same.\n\n## User Docs\n\nThis is a pure python development kit for interacting with the Iterable API. If you find anything to be out of date or are looking for support, you can file an issue on Github.\n\n### Installation\n\nYou can download and install the package from the Python Package Index with:\n\n```\npip install iterable-api\n```\n\n### Quickstart\n\n```py\nfrom iterable import Iterable\n\napi = Iterable('YOUR_API_KEY')\n\napi.events.track(event_name='hello_iterable', user_id=42, created_at=datetime.now().to_timestamp())\n```\n\nIf you're familiar with environment variables, you can set `ITERABLE_API_KEY`. In that case you can set up the api client like so:\n\n```py\nfrom os import getenv\nfrom iterable import Iterable\n\napi = Iterable(getenv('ITERABLE_API_KEY'))\n```\n\n### Data exports\n\nIf you're interested in getting data out of your Iterable account, you can use the `export_data_api` method on the API client.\n\n### Dropping down\n\nThe API client is a requests.Session under the hood with HTTP method names as top level functions in the wrapper.\n\nIf you want to drop down to the client, you only need to provide the resource path, e.g.:\n\n```py\napi.get('/events/track')\n```\n\nThis might be useful for exploring the API or debugging an issue.\n\n## Development Docs\n\nIf you're interested in extending this library, please follow these guidelines:\n\n1. Please file an issue first describing what you want to add or change.\n2. Fork the repository and submit a pull request.\n\n### Installation for development\n\nThis project uses Pipenv for now, so follow your preferred procedure for that.\n\n```\npipenv install\npipenv install -e .\n```\n\n### Testing\n\nThe library uses pytest - you can run the tests by invoking the following:\n\n```py\npytest\n```\n",
    'author': 'Alex Kahn',
    'author_email': 'alexkahn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alexkahn/iterable-api',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
