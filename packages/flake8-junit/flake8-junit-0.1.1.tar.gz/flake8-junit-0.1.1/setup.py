# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['flake8_junit']
install_requires = \
['flake8>=3.0', 'pycodestyle']

entry_points = \
{'flake8.extension': ['J10 = flake8_junit:AssertChecker']}

setup_kwargs = {
    'name': 'flake8-junit',
    'version': '0.1.1',
    'description': 'JUnit assert statement checker plugin for flake8',
    'long_description': 'Flake8 JUnit asserts plugin\n===========================\n\nCheck for JUnit assert statements in your tests.\n\nThis module provides a plugin for ``flake8``, the Python code checker.\n\n\nInstallation\n------------\n\nYou can install or upgrade ``flake8-junit`` with these commands::\n\n  $ pip install flake8-junit\n  $ pip install --upgrade flake8-junit\n\n\nPlugin for Flake8\n-----------------\n\nWhen both ``flake8`` and ``flake8-junit`` are installed, the plugin is\navailable in ``flake8``::\n\n    $ flake8 --version\n    5.0.4 (flake8-junit: 0.1.0, mccabe: 0.7.0, pycodestyle: 2.9.1, pyflakes: 2.5.0) CPython 3.9.9 on Darwin\n\nFlake8 allows disabling some tests based on the folder:\n\n```\n[flake8]\nper-file-ignores =\n    tests/accounting/*: J10\n```\n\nError codes\n-----------\n\n| Error Code  | Description                          |\n| ----------- | ------------------------------------ |\n| J100        | JUnit assert found                   |\n\n\nChanges\n-------\n\n##### 0.1.1 - 2022-09-09\n\n* First public release\n',
    'author': 'Pablo Marti Gamboa',
    'author_email': 'pablo@cointracker.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/coin-tracker/flake8-junit',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
