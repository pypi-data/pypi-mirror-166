# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moonpies']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3,<4.0', 'numpy>=1.17,<2.0', 'pandas>=1.0,<2.0']

entry_points = \
{'console_scripts': ['moonpies = moonpies.cli:run']}

setup_kwargs = {
    'name': 'moonpies',
    'version': '1.0.0',
    'description': 'Moon Polar Ice and Ejecta Stratigraphy model',
    'long_description': None,
    'author': 'Christian J. Tai Udovicic',
    'author_email': 'cjtu@nau.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
