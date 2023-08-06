# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylanggetter']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0']

entry_points = \
{'console_scripts': ['pylanggetter = pylanggetter.pylanggetter:start']}

setup_kwargs = {
    'name': 'pylanggetter',
    'version': '0.2.8',
    'description': 'Tiny utility to help you download Dofus Retro Lang files',
    'long_description': '# PyLangGetter\nTiny utility to help you download Dofus Retro Lang files.\n\n# Installation\n`pip install pylanggetter`\n\n## Usage\n`python -m pylanggetter` to get all lang files in all language \\\n`python -m pylanggetter fr` to get lang files in **fr** language \\\n`python -m pylanggetter it de` to get lang files in **it** and **de** langage \\\nAvailable language option : `fr, de, en, it, es, pt, nl`',
    'author': 'Dysta',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Dysta/PylangGetter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
