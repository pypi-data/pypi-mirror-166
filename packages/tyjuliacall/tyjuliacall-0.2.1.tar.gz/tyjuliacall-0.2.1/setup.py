# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tyjuliacall', 'tyjuliasetup']

package_data = \
{'': ['*'], 'tyjuliasetup': ['src/*']}

install_requires = \
['julia-numpy>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['mk-ty-sysimage = tyjuliasetup.cli:mkimage']}

setup_kwargs = {
    'name': 'tyjuliacall',
    'version': '0.2.1',
    'description': 'A Python package for Tongyuan-hacked PyCall as an engineerization for Python-Julia interops.',
    'long_description': None,
    'author': 'Suzhou-Tongyuan',
    'author_email': 'support@tongyuan.cc',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
