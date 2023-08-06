# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['circe']

package_data = \
{'': ['*'], 'circe': ['static/*']}

install_requires = \
['aiofiles>=0.8.0,<0.9.0',
 'argh>=0.26.2,<0.27.0',
 'asyncio>=3.4.3,<4.0.0',
 'huey>=2.4.3,<3.0.0',
 'itsdangerous>=2.1.2,<3.0.0',
 'markdown2>=2.4.3,<3.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'python-json-logger>=2.0.2,<3.0.0',
 'requests>=2.28.0,<3.0.0',
 'sanic>=22.3.2,<23.0.0']

entry_points = \
{'console_scripts': ['circe = circe.__main__:run_cli']}

setup_kwargs = {
    'name': 'circe-certic',
    'version': '0.0.37',
    'description': 'Circe Server',
    'long_description': None,
    'author': 'Mickaël Desfrênes',
    'author_email': 'mickael.desfrenes@unicaen.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
