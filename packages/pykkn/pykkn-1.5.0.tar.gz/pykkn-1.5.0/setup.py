# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pykkn', 'pykkn.components', 'pykkn.utils']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.2.0,<10.0.0',
 'h5py>=3.7.0,<4.0.0',
 'numpy>=1.23.2,<2.0.0',
 'opencv-python>=4.6.0,<5.0.0',
 'pytest>=7.1.3,<8.0.0']

setup_kwargs = {
    'name': 'pykkn',
    'version': '1.5.0',
    'description': '',
    'long_description': None,
    'author': 'Martin Hock',
    'author_email': 'Martin.Hock@fst.tu-darmstadt.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
