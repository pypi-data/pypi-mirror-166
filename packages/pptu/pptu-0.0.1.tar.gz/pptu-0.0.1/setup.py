# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pptu']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pptu',
    'version': '0.0.1',
    'description': 'Reserved',
    'long_description': 'None',
    'author': 'nyuszika7h',
    'author_email': 'nyuszika7h@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
