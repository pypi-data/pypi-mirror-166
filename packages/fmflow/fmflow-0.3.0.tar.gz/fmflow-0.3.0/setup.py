# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fmflow',
 'fmflow.core',
 'fmflow.core.array',
 'fmflow.core.cube',
 'fmflow.core.spectrum',
 'fmflow.fits',
 'fmflow.fits.aste',
 'fmflow.fits.nro45m',
 'fmflow.logging',
 'fmflow.models',
 'fmflow.models.astrosignal',
 'fmflow.models.atmosphere',
 'fmflow.models.commonmode',
 'fmflow.models.gain',
 'fmflow.utils',
 'fmflow.utils.binary',
 'fmflow.utils.convergence',
 'fmflow.utils.datetime',
 'fmflow.utils.fits',
 'fmflow.utils.misc',
 'fmflow.utils.ndarray']

package_data = \
{'': ['*'], 'fmflow': ['data/*']}

install_requires = \
['matplotlib>=3.2,<4.0',
 'netcdf4>=1.6,<2.0',
 'numba>=0.56,<0.57',
 'pyyaml>=6.0,<7.0',
 'tqdm>=4.64,<5.0']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['astropy>=4.3,<5.0',
                                                         'numpy>=1.21,<1.22',
                                                         'scikit-learn>=1.0,<1.1',
                                                         'scipy>=1.7,<1.8',
                                                         'xarray>=0.20,<0.21'],
 ':python_version >= "3.8" and python_version < "3.11"': ['astropy>=5.0,<6.0',
                                                          'numpy>=1.22,<2.0',
                                                          'scikit-learn>=1.1,<2.0',
                                                          'scipy>=1.8,<2.0',
                                                          'xarray>=0.21,<2023']}

setup_kwargs = {
    'name': 'fmflow',
    'version': '0.3.0',
    'description': 'Data analysis package for FMLO',
    'long_description': '# fmflow\n\n[![Release](https://img.shields.io/pypi/v/fmflow?label=Release&color=cornflowerblue&style=flat-square)](https://pypi.org/project/fmflow/)\n[![Python](https://img.shields.io/pypi/pyversions/fmflow?label=Python&color=cornflowerblue&style=flat-square)](https://pypi.org/project/fmflow/)\n[![Downloads](https://img.shields.io/pypi/dm/fmflow?label=Downloads&color=cornflowerblue&style=flat-square)](https://pepy.tech/project/fmflow)\n[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.3433962-cornflowerblue?style=flat-square)](https://doi.org/10.5281/zenodo.3433962)\n[![Tests](https://img.shields.io/github/workflow/status/fmlo-dev/fmflow/Tests?label=Tests&style=flat-square)](https://github.com/fmlo-dev/fmflow/actions)\n\nData analysis package for FMLO\n',
    'author': 'Akio Taniguchi',
    'author_email': 'taniguchi@a.phys.nagoya-u.ac.jp',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/astropenguin/fmflow/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
