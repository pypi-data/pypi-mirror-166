# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dpvs']

package_data = \
{'': ['*']}

install_requires = \
['hydra-core>=1.2.0,<2.0.0', 'ipython>=8.5.0,<9.0.0']

setup_kwargs = {
    'name': 'dpvs',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'dennislblog',
    'author_email': 'dennisl@udel.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
