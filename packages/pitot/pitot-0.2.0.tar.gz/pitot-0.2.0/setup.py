# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pitot']

package_data = \
{'': ['*']}

install_requires = \
['Pint-Pandas>=0.2,<0.3',
 'Pint>=0.19.2,<0.20.0',
 'numpy>=1.23.0,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'pyproj>=3.3.1,<4.0.0',
 'typing-extensions>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'pitot',
    'version': '0.2.0',
    'description': 'Toolbox for aeronautic units and conversions',
    'long_description': '# pitot\n\n[![tests](https://github.com/atmdata/pitot/actions/workflows/run-tests.yml/badge.svg)](https://github.com/atmdata/pitot/actions/workflows/run-tests.yml)\n[![Code Coverage](https://img.shields.io/codecov/c/github/atmdata/pitot.svg)](https://codecov.io/gh/atmdata/pitot)\n[![Checked with mypy](https://img.shields.io/badge/mypy-checked-blue.svg)](https://mypy.readthedocs.io/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/psf/black)\n![License](https://img.shields.io/pypi/l/pitot.svg)\\\n![PyPI version](https://img.shields.io/pypi/v/pitot)\n[![PyPI downloads](https://img.shields.io/pypi/dm/pitot)](https://pypi.org/project/pitot)\n![Conda version](https://img.shields.io/conda/vn/conda-forge/pitot)\n[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/pitot.svg)](https://anaconda.org/conda-forge/pitot)\n\npitot is a Python toolbox providing efficient aeronautic calculations.\n\nImplementations are:\n\n- **efficient**, based on NumPy or state-of-the-art libraries;\n- provided with **typing stubs**;\n- unambiguous with **physical units**, with the help of the [`pint`](https://pint.readthedocs.io/) library.  \n  All parameters may be passed with or without a physical unit (default units are explicit in the documentation), but all return values come with a physical unit.\n\nThe following functions are currently available:\n\n- International Standard Atmosphere (temperature, density, pressure and speed of sound);\n- conversions between various air speeds: CAS, TAS, EAS and Mach number;\n- geodetic calculations (distance, bearing, great circle, etc.) on a WGS84 ellipsoid.\n\n## Installation\n\n### Latest release\n\n```sh\npip install pitot\n```\n\n### Development version\n\n```sh\npoetry install\n```\n\n## Basic usage\n\nPhysical units are not mandatory for arguments, but return values are all [`pint`](https://pint.readthedocs.io/) quantities\n\n```pycon\n>>> from pitot.isa import temperature\n>>> temperature(0)\nDefault unit [m] will be used for argument \'h\'.\n<Quantity(288.15, \'kelvin\')>\n>>> temperature([0, 1000])\nDefault unit [m] will be used for argument \'h\'.\n<Quantity([288.15 281.65], \'kelvin\')>\n```\n\nYou may access the value with the `m` (stands for _magnitude_) attribute:\n\n```pycon\n>>> temperature(0).m  # in Kelvin by default\nDefault unit [m] will be used for argument \'h\'.\n288.15\n>>> temperature(0).to("°C").m\nDefault unit [m] will be used for argument \'h\'.\n15.0\n```\n\nIt is preferable to avoid warnings by passing values with a physical unit:\n\n```pycon\n>>> from pitot import Q_\n>>> temperature(Q_([0, 1000], "ft")).to("°C")\n<Quantity([15.     13.0188], \'degree_Celsius\')>\n```\n\nThings also work with NumPy arrays...\n\n```pycon\n>>> import numpy as np\n>>> temperature(Q_(np.array([0, 1000]), "ft"))\n<Quantity([288.15   286.1688], \'kelvin\')>\n>>> temperature(Q_(np.array([0, 1000]), "ft")).to("°C").m\narray([15.    , 13.0188])\n```\n\n... or with Pandas Series:\n\n```pycon\n>>> import pandas as pd\n>>> temperature(pd.Series([0., 1000], dtype="pint[ft]")).pint.to("°C")\n0                  15.0\n1    13.018799999999999\ndtype: pint[°C]\n```\n\n## Contributions\n\nAny input, feedback, bug report or contribution is welcome.\n\nBefore opening a PR, please check your commits follow a number of safeguards with hooks to install as follow:\n\n```sh\npoetry run pre-commit install\n```\n\nThen you should prefix you `git commit` commands as follow:\n\n```sh\npoetry run git commit -m "fantastic commit message"\n```\n',
    'author': 'Xavier Olive',
    'author_email': 'git@xoolive.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
