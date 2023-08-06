# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datastuff']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.4,<2.0.0']

setup_kwargs = {
    'name': 'datastuff',
    'version': '0.1.0',
    'description': 'A package that provides functions for a collection of common data science tasks',
    'long_description': None,
    'author': 'benthecoder',
    'author_email': 'benthecoder07@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
