# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atcommander']

package_data = \
{'': ['*']}

install_requires = \
['pyserial>=3.5,<4.0', 'requests>=2.28.1,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['atc = atcommander:app']}

setup_kwargs = {
    'name': 'atcommander',
    'version': '0.1.0',
    'description': 'A simple AT Command tool',
    'long_description': '# ATCommander\n',
    'author': 'helloysd',
    'author_email': 'helloysd@foxmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
