# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymarble',
 'pymarble.backend',
 'pymarble.frontend',
 'pymarble.frontend.static',
 'pymarble.frontend.view']

package_data = \
{'': ['*'], 'pymarble.frontend.static': ['images/*']}

install_requires = \
['PyQt5>=5.15.6,<6.0.0',
 'h5py>=3.6.0,<4.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'pandas>=1.4.1,<2.0.0',
 'prettytable>=3.2.0,<4.0.0',
 'sortedcontainers>=2.4.0,<3.0.0']

entry_points = \
{'console_scripts': ['marble-cli = pymarble.rff:main',
                     'marble-gui = pymarble.frontend.app:main']}

setup_kwargs = {
    'name': 'pymarble',
    'version': '0.9.0',
    'description': '',
    'long_description': None,
    'author': 'Dr. Steffen Brinckmann',
    'author_email': 's.brinckmann@fz-juelich.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
