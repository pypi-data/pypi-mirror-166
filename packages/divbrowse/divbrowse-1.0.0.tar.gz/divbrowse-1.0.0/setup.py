# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['divbrowse', 'divbrowse.lib']

package_data = \
{'': ['*'], 'divbrowse': ['tests/data/*']}

install_requires = \
['bioblend>=0.16.0,<0.17.0',
 'click>=8.0.1,<9.0.0',
 'flask>=2.0.1,<3.0.0',
 'numpy>=1.21.1,<2.0.0',
 'pandas>=1.3.0,<2.0.0',
 'pyyaml>=5.4.1,<6.0.0',
 'scikit-allel>=1.3.5,<2.0.0',
 'scikit-learn>=0.24.2,<0.25.0',
 'simplejson>=3.17.3,<4.0.0',
 'tables>=3.6.1,<4.0.0',
 'umap-learn>=0.5.2,<0.6.0',
 'waitress==2.0.0',
 'zarr>=2.8.3,<3.0.0']

extras_require = \
{'docs': ['sphinx>=4.0.2,<5.0.0',
          'sphinx-autoapi>=1.6.0,<2.0.0',
          'sphinx_rtd_theme>=0.5.2,<0.6.0',
          'sphinx-click>=3.0.1,<4.0.0']}

entry_points = \
{'console_scripts': ['divbrowse = divbrowse.cli:main']}

setup_kwargs = {
    'name': 'divbrowse',
    'version': '1.0.0',
    'description': 'A web application for interactive visualization and analysis of genotypic variant matrices',
    'long_description': None,
    'author': 'Patrick König',
    'author_email': 'koenig@ipk-gatersleben.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
