# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cryptmoji']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cryptmoji',
    'version': '0.1.0',
    'description': 'Encrypt Text using emojis!',
    'long_description': None,
    'author': 'Siddhesh Agarwal',
    'author_email': 'siddhesh.agarwal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
