# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hypermodern_cookiecutter_example']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1']

entry_points = \
{'console_scripts': ['hypermodern-cookiecutter-example = '
                     'hypermodern_cookiecutter_example.__main__:main']}

setup_kwargs = {
    'name': 'hypermodern-cookiecutter-example',
    'version': '0.0.0',
    'description': 'Hypermodern Cookiecutter Example',
    'long_description': "# Hypermodern Cookiecutter Example\n\n[![PyPI](https://img.shields.io/pypi/v/hypermodern-cookiecutter-example.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/hypermodern-cookiecutter-example.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/hypermodern-cookiecutter-example)][python version]\n[![License](https://img.shields.io/pypi/l/hypermodern-cookiecutter-example)][license]\n\n[![Read the documentation at https://hypermodern-cookiecutter-example.readthedocs.io/](https://img.shields.io/readthedocs/hypermodern-cookiecutter-example/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/paulrousset/hypermodern-cookiecutter-example/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/paulrousset/hypermodern-cookiecutter-example/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/hypermodern-cookiecutter-example/\n[status]: https://pypi.org/project/hypermodern-cookiecutter-example/\n[python version]: https://pypi.org/project/hypermodern-cookiecutter-example\n[read the docs]: https://hypermodern-cookiecutter-example.readthedocs.io/\n[tests]: https://github.com/paulrousset/hypermodern-cookiecutter-example/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/paulrousset/hypermodern-cookiecutter-example\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _Hypermodern Cookiecutter Example_ via [pip] from [PyPI]:\n\n```console\n$ pip install hypermodern-cookiecutter-example\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Hypermodern Cookiecutter Example_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/paulrousset/hypermodern-cookiecutter-example/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/paulrousset/hypermodern-cookiecutter-example/blob/main/LICENSE\n[contributor guide]: https://github.com/paulrousset/hypermodern-cookiecutter-example/blob/main/CONTRIBUTING.md\n[command-line reference]: https://hypermodern-cookiecutter-example.readthedocs.io/en/latest/usage.html\n",
    'author': 'Paul Rousset',
    'author_email': 'paulrousset@hotmail.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/paulrousset/hypermodern-cookiecutter-example',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
