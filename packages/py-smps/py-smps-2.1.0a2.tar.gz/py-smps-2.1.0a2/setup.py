# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['smps']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.0,<2.0',
 'numpy>=1.23.2,<2.0.0',
 'pandas>=1.4,<2.0',
 'requests>=2.24,<3.0',
 'scipy>=1.9,<2.0',
 'seaborn>=0.11.0,<0.12.0',
 'setuptools>=65.0,<66.0',
 'statsmodels>=0.13,<0.14']

setup_kwargs = {
    'name': 'py-smps',
    'version': '2.1.0a2',
    'description': 'A simple python library to import and visualize data from particle sizing instruments.',
    'long_description': '[![PyPI version](https://badge.fury.io/py/py-smps.svg)](https://badge.fury.io/py/py-smps)\n[![Build Status](https://travis-ci.org/dhhagan/py-smps.svg?branch=master)](https://travis-ci.org/dhhagan/py-smps)\n[![Coverage Status](https://coveralls.io/repos/github/dhhagan/py-smps/badge.svg?branch=master)](https://coveralls.io/github/dhhagan/py-smps?branch=master)\n\n\n# py-smps\nPython library for the analysis and visualization of data from a Scanning Mobility Particle Sizer (SMPS) and other particle sizing instruments (SEMS, OPC\'s).\n\n## Dependencies\n\nThe full list of dependencies can be found in the `pyproject.toml` file and are summarized below:\n\n```py\npython = ">=3.8, <3.12"\nstatsmodels = "^0.13"\nseaborn = "^0.10"\njoblib = "^1.0"\nrequests = "^2.24"\nscipy = "^1.9"\nnumpy = "^1.23.2"\npandas = "^1.4"\n```\n\nAs of `v1.2.0a0`, the library should be compatible with Apple silicone (tested on both M1 and M2).\n\n## Python Versions\n\nPython3.8 through Python3.11 are currently supported.\n\n## Installation\n\nTo install from PyPi:\n\n    $ pip install py-smps [--upgrade]\n\nIf you\'d like the latest pre-release:\n\n    $ pip install py-smps --pre [--upgrade]\n\nTo install the edge release directly from GitHub:\n\n    pip install git+https://github.com/quant-aq/py-smps.git\n\n## Unittests\n\nUnittests can be run by issuing the following command from within the main repo:\n\n```sh\n$ poetry run pytest -s tests/ --ignore=tests/datafiles\n```\n\n\n## Documentation\n\nDocumentation is available [here](https://quant-aq.github.io/py-smps/). Docs are built using Sphinx and can be built locally by doing the following:\n\n```sh\n$ cd docs/\n$ make clean\n$ make guides\n$ make html\n$ cd ..\n```\n\nThen, you can navigate to your local directory at `docs/_build/html/` and open up the `index.html` file in your preferred browser window.\n\n\n## Contributing to Development\n\nWe welcome all contributions from the community in the form of issues reporting, feature requests, bug fixes, etc.\n\nIf there is a feature you would like to see or a bug you would like to report, please open an issue. We will try to get to things as promptly as possible. Otherwise, feel free to send PR\'s!\n\n\n## Colorbar Information\n\n  * [matplotlib colorbars](http://matplotlib.org/examples/color/colormaps_reference.html)\n  * [seaborn color palette](http://seaborn.pydata.org/tutorial/color_palettes.html)\n\n',
    'author': 'David H Hagan',
    'author_email': 'david.hagan@quant-aq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/quant-aq/py-smps',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
