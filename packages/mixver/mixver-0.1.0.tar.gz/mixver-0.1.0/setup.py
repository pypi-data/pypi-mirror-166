# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mixver', 'mixver.storages', 'mixver.versioning']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mixver',
    'version': '0.1.0',
    'description': 'Custom versioning of ML models',
    'long_description': None,
    'author': 'hectorLop',
    'author_email': 'lopez.almazan.hector@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
