# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['packages_farrukh90']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'packages-farrukh90',
    'version': '0.2.0',
    'description': '',
    'long_description': '',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
