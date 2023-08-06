# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_example_server', 'fastapi_example_server.models']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=14.2.0,<15.0.0', 'fastapi[all]>=0.81.0,<0.82.0']

entry_points = \
{'console_scripts': ['doc = fastapi_example_server.doc:main',
                     'main = fastapi_example_server.main:main']}

setup_kwargs = {
    'name': 'fastapi-example-server',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Julian Lechner',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10.6,<4.0.0',
}


setup(**setup_kwargs)
