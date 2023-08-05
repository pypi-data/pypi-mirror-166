# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['scatsol']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.3,<4.0.0', 'numpy>=1.23.2,<2.0.0', 'scipy>=1.9.1,<2.0.0']

setup_kwargs = {
    'name': 'scatsol',
    'version': '0.0.2',
    'description': '',
    'long_description': None,
    'author': 'tiagovla',
    'author_email': 'tiagovla@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
