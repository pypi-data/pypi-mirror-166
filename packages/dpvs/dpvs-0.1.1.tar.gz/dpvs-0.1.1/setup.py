# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dpvs', 'dpvs.configs', 'dpvs.logging', 'dpvs.plugins']

package_data = \
{'': ['*']}

install_requires = \
['hydra-core>=1.2.0,<2.0.0', 'ipython>=8.5.0,<9.0.0']

setup_kwargs = {
    'name': 'dpvs',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Installation\n```bash\n# install package\npip install dpvs\n# install torch\ngo to /bin/install.sh and change torch according to your cuda version\nnvcc --version \nsh bin/install.sh\n```',
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
