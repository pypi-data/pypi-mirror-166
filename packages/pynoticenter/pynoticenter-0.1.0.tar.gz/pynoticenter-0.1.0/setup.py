# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pynoticenter']

package_data = \
{'': ['*']}

install_requires = \
['asyncio>=3.4.3,<4.0.0']

entry_points = \
{'console_scripts': ['demo = src.example.demo:main']}

setup_kwargs = {
    'name': 'pynoticenter',
    'version': '0.1.0',
    'description': 'Python client side notification center.',
    'long_description': '# pynoticenter\nPython client notification center.\n',
    'author': 'dzhsurf',
    'author_email': 'dzhsurf@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dzhsurf/pynoticenter',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
