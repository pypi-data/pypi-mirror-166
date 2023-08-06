# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['candyland']

package_data = \
{'': ['*']}

install_requires = \
['numpy', 'plotly', 'pydantic']

setup_kwargs = {
    'name': 'candyland',
    'version': '0.1.0',
    'description': 'Candyland is a simple python package for quickly processing data-streams',
    'long_description': '',
    'author': 'FL03',
    'author_email': 'jo3mccain@icloud.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/FL03/candyland',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
