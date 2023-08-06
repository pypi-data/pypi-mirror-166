# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cryptmoji']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cryptmoji',
    'version': '1.1.1',
    'description': 'Encrypt Text using emojis!',
    'long_description': '# Cryptmoji\n\nA simple emoji-based encryption algorithm.\n_______________________\n\n## Installation\n\npip install the library:\n\n```sh\npip install cryptmoji\n```\n\n## Usage\n\n```python\nfrom cryptmoji import Cryptmoji\n\ntext = "Hello World!"\nkey = "random_key" # makes the encryption stronger (optional)\na = Cryptmoji(text, key=key)\nencrypted = a.encrypt()\nprint(encrypted)\ndecrypted = a.decrypt()\nprint(decrypted)\n```\n',
    'author': 'Siddhesh Agarwal',
    'author_email': 'siddhesh.agarwal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Siddhesh-Agarwal/cryptmoji',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
