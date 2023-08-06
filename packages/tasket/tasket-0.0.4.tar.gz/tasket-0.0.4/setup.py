# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tasket']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.40,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'coverage[toml]>=6.4.4,<7.0.0',
 'rich>=12.5.1,<13.0.0',
 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['tasket = tasket.main:app']}

setup_kwargs = {
    'name': 'tasket',
    'version': '0.0.4',
    'description': 'Maintain a list of needful things to do.',
    'long_description': None,
    'author': 'Damien Calloway',
    'author_email': 'damiencalloway@fastmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
