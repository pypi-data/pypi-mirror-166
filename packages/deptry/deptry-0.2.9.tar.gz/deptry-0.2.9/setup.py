# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deptry', 'deptry.issue_finders']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'isort>=5.10.1,<6.0.0', 'toml>=0.10.2,<0.11.0']

extras_require = \
{':python_version <= "3.7"': ['importlib-metadata']}

entry_points = \
{'console_scripts': ['deptry = deptry.cli:deptry']}

setup_kwargs = {
    'name': 'deptry',
    'version': '0.2.9',
    'description': 'A command line utility to check for obsolete, missing and transitive dependencies in a poetry managed python project.',
    'long_description': "# deptry\n\n[![Release](https://img.shields.io/github/v/release/fpgmaas/deptry)](https://img.shields.io/github/v/release/fpgmaas/deptry)\n[![Build status](https://img.shields.io/github/workflow/status/fpgmaas/deptry/merge-to-main)](https://img.shields.io/github/workflow/status/fpgmaas/deptry/merge-to-main)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/deptry)](https://pypi.org/project/deptry/)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/deptry)](https://img.shields.io/pypi/dm/deptry?style=flat-square)\n[![License](https://img.shields.io/github/license/fpgmaas/deptry)](https://img.shields.io/github/license/fpgmaas/deptry)\n\n---\n\n_deptry_ is a command line tool to check for issues with dependencies in a poetry managed Python project. It checks for four types of issues:\n\n- Obsolete dependencies: Dependencies which are added to your project's dependencies, but which are not used within the codebase.\n- Missing dependencies: Modules that are imported within your project, but no corresponding package is found in the environment.\n- Transitive dependencies: Packages from which code is imported, but the package (A) itself is not in your projects dependencies. Instead, another package (B) is in your list of dependencies, which depends on (A). Package (A) should be added to your project's list of dependencies.\n- Misplaced dependencies: Development dependencies that should be included as regular dependencies.\n\n_deptry_ detects these issue by scanning the imported modules within all Python files in \na directory and it's subdirectories, and comparing those to the dependencies listed in _pyproject.toml_.\n\n---\n\n**Documentation**: <https://fpgmaas.github.io/deptry/>\n\n---\n\n## Quickstart\n\n### Installation\n\n_deptry_ can be added to your project with \n\n```\npoetry add --group dev deptry\n```\n\nor for older versions of poetry:\n\n```\npoetry add --dev deptry\n```\n\n### Prerequisites\n\nIn order to check for obsolete imports, _deptry_ requires a _pyproject.toml_ file to be present in the directory passed as the first argument, and it requires the corresponding environment to be activated.\n\n### Usage\n\nTo scan your project for obsolete imports, run\n\n```sh\ndeptry .\n```\n\n__deptry__ can be configured by using additional command line arguments, or \nby adding a `[tool.deptry]` section in __pyproject.toml__.\n\nFor more information, see the [documentation](https://fpgmaas.github.io/deptry/).\n\n---\n\nRepository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).",
    'author': 'Florian Maas',
    'author_email': 'fpgmaas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fpgmaas/deptry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
