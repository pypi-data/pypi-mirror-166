# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imreco']

package_data = \
{'': ['*']}

install_requires = \
['opencv-python>=4.6.0,<5.0.0']

setup_kwargs = {
    'name': 'imreco',
    'version': '0.1.0',
    'description': 'A python cli program to perform basic operations to images using opencv.',
    'long_description': None,
    'author': 'tamton-aquib',
    'author_email': 'aquibjavedt007@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
