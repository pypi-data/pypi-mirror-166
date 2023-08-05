# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylanggetter']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0']

entry_points = \
{'console_scripts': ['pylanggetter = pylanggetter.PylangGetter:start']}

setup_kwargs = {
    'name': 'pylanggetter',
    'version': '0.1.0',
    'description': 'Tiny utility to help you download Dofus Retro Lang files',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
