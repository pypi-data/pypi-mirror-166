# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylanggetter']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'pylanggetter',
    'version': '0.2.1',
    'description': 'Tiny utility to help you download Dofus Retro Lang files',
    'long_description': '# PyLangGetter\nTiny utility to help you download Dofus Retro Lang files.\n\n## Usage\n`python PyLangGetter.py` to get all lang files in all language \\\n`python PyLangGetter.py fr` to get lang files in **fr** language \\\n`python PylangGetter.py it de` to get lang files in **it** and **de** langage \\\nAvailable language option : `fr, de, en, it, es, pt, nl`',
    'author': 'Dysta',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Dysta/PylangGetter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
