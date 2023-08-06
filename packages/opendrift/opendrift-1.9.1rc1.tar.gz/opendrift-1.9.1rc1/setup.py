# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opendrift',
 'opendrift.elements',
 'opendrift.export',
 'opendrift.models',
 'opendrift.models.eulerdrift',
 'opendrift.models.openoil',
 'opendrift.models.openoil.adios',
 'opendrift.models.openoil.adios.computation',
 'opendrift.models.openoil.adios.extra_oils',
 'opendrift.models.openoil.adios.extra_oils.templates',
 'opendrift.models.openoil.adios.models',
 'opendrift.models.openoil.adios.models.common',
 'opendrift.models.openoil.adios.models.oil',
 'opendrift.models.openoil.adios.models.oil.cleanup',
 'opendrift.models.openoil.adios.models.oil.validation',
 'opendrift.models.openoil.adios.util',
 'opendrift.readers',
 'opendrift.readers.basereader',
 'opendrift.readers.interpolation',
 'opendrift.readers.operators',
 'opendrift.readers.roppy',
 'opendrift.readers.unstructured',
 'opendrift.scripts']

package_data = \
{'': ['*']}

install_requires = \
['Cartopy>=0.20',
 'cmocean>=2.0,<3.0',
 'coloredlogs>=15.0.1,<16.0.0',
 'geojson>=2.5.0,<3.0.0',
 'matplotlib>=3.5',
 'nc-time-axis>=1.4.1,<2.0.0',
 'netCDF4>=1.6',
 'numpy>=1.23',
 'pynucos>=3',
 'pyproj>=2.3',
 'requests>=2.28.1,<3.0.0',
 'roaring-landmask>=0.5.1',
 'scipy>=1.9',
 'utm>=0.7.0,<0.8.0',
 'xarray>=2022.6.0']

extras_require = \
{'grib': ['cfgrib>=0.9.10,<0.10.0', 'pygrib>=2.1.4,<3.0.0']}

setup_kwargs = {
    'name': 'opendrift',
    'version': '1.9.1rc1',
    'description': 'OpenDrift - a framework for ocean trajectory modeling',
    'long_description': None,
    'author': 'Knut-Frode Dagestad',
    'author_email': 'knutfd@met.no>, Gaute Hope <gauteh@met.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
