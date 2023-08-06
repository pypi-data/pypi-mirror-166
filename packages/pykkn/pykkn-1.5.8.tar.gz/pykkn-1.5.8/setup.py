# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pykkn']

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
    'version': '1.5.8',
    'description': 'Python port of the matlab library kkn https://git.rwth-aachen.de/nils.preuss/rdm-kraken/',
    'long_description': '# pykkn\n\nPYKKN is a library that supports researchers to store their data in a HDF5 file using Python. The library can handle different types of inputs like array, matrix, image and video.\n\n## Documentation\nThe documentation can be found [here](https://fst-tuda.pages.rwth-aachen.de/public/pykkn/).\n\n# Repository\nhttps://git.rwth-aachen.de/fst-tuda/public/pykkn',
    'author': 'Martin Hock',
    'author_email': 'Martin.Hock@fst.tu-darmstadt.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://fst-tuda.pages.rwth-aachen.de/public/pykkn/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
