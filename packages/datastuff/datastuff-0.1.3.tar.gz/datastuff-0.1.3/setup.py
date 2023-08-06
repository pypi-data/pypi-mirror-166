# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datastuff']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.2,<2.0.0', 'pandas>=1.4.4,<2.0.0']

setup_kwargs = {
    'name': 'datastuff',
    'version': '0.1.3',
    'description': 'A package that provides functions for a collection of common data science tasks',
    'long_description': "# datastuff\n\nA simple python package that provides functions for a collection of common data science tasks\n\n[![PyPI Version][pypi-image]][pypi-url]\n[![Build Status][build-image]][build-url]\n[![Code Coverage][coverage-image]][coverage-url]\n[![][stars-image]][stars-url]\n\n## Getting started\n\nYou can [get `datastuff` from PyPI](https://pypi.org/project/datastuff),\nwhich means it's easily installable with `pip`:\n\n```bash\npip install datastuff\n```\n\n## Changelog\n\nRefer to the [CHANGELOG.rst](CHANGELOG.rst) file.\n\n<!-- Badges: -->\n\n[pypi-image]: https://img.shields.io/pypi/v/datastuff\n[pypi-url]: https://pypi.org/project/datastuff/\n[build-image]: https://github.com/benthecoder/datastuff/actions/workflows/build.yaml/badge.svg\n[build-url]: https://github.com/benthecoder/datastuff/actions/workflows/build.yaml\n[coverage-image]: https://codecov.io/gh/benthecoder/datastuff/branch/main/graph/badge.svg\n[coverage-url]: https://codecov.io/gh/benthecoder/datastuff/\n[stars-image]: https://img.shields.io/github/stars/benthecoder/datastuff/\n[stars-url]: https://github.com/benthecoder/datastuff\n",
    'author': 'benthecoder',
    'author_email': 'benthecoder07@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
