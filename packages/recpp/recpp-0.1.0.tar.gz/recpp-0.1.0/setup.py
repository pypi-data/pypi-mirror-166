# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['recpp']

package_data = \
{'': ['*']}

install_requires = \
['pcpp>=1.30,<2.0']

entry_points = \
{'console_scripts': ['recpp = recpp.cli:main']}

setup_kwargs = {
    'name': 'recpp',
    'version': '0.1.0',
    'description': '',
    'long_description': '# ReCPP\n\nC Preprocessor for Reverse Engineering\n\nThis is a fork of pcpp, the Python-based C preprocessor, with modifications to help with reverse engineering.\n\nI may expand & rewrite some preprocessing logic in the future, but at the moment, I just have a change hard-coded that helps me solve a particular problem.\n',
    'author': 'Andrew Elgert',
    'author_email': 'andrew.elgert@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
