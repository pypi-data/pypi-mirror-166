# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_dhos']

package_data = \
{'': ['*']}

extras_require = \
{'fbi': ['flask_batteries_included'], 'neo': ['neomodel']}

entry_points = \
{'pytest11': ['pytest_dhos = pytest_dhos']}

setup_kwargs = {
    'name': 'pytest-dhos',
    'version': '1.0.5',
    'description': 'Common fixtures for pytest in DHOS services and libraries',
    'long_description': None,
    'author': 'Duncan Booth',
    'author_email': 'duncan.booth@sensynehealth.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/polaris-foundation/pytest-dhos',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
