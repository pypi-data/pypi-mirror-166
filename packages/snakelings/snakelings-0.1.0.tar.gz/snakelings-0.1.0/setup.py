# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snakelings']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'click-default-group>=1.2.2,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'pydantic>=1.10.1,<2.0.0',
 'pytest>=7.1.3,<8.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.5.1,<13.0.0',
 'watchdog>=2.1.9,<3.0.0']

entry_points = \
{'console_scripts': ['snakelings = snakelings:cli']}

setup_kwargs = {
    'name': 'snakelings',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Chris Blades',
    'author_email': 'chrisdblades@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
