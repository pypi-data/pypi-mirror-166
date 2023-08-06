# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['redstone_computer_utilities']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.5,<0.5.0', 'typing-extensions>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'redstone-computer-utilities',
    'version': '0.2.0.post3',
    'description': 'Lightweight and Modular Redstone Computer Debugging Tools.',
    'long_description': '<img src="https://cdn.jsdelivr.net/gh/NKID00/redstone-computer-utilities@dev/src/main/resources/assets/rcutil/icon.png" alt="icon" align="right" height="175">\n\n# Redstone Computer Utilities\n\n>  Lightweight and Modular Redstone Computer Debugging Tools.\n\n## Installation\n\nPython 3.7.2 or newer (CPython or PyPy) is required.\n\n```sh\n$ pip install redstone-computer-utilities\n```\n\nor\n\n```toml\n# pyproject.toml\nredstone-computer-utilities = "^0.2.0"\n```\n\n### Check the GitHub repository [NKID00/redstone-computer-utilities](https://github.com/NKID00/redstone-computer-utilities) for details.',
    'author': 'NKID00',
    'author_email': 'nkid00@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NKID00/redstone-computer-utilities',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
