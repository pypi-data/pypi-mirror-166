# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_tictoc_timer']

package_data = \
{'': ['*']}

install_requires = \
['typeguard>=2.13,<2.14']

setup_kwargs = {
    'name': 'py-tictoc-timer',
    'version': '0.1.13',
    'description': "Time the execution of Python code using syntax similar to MATLAB's tic and toc functions.",
    'long_description': '# py-tictoc-timer\n\n[![codecov](https://codecov.io/gh/chrimaho/py-tictoc-timer/branch/main/graph/badge.svg)](https://codecov.io/gh/chrimaho/py-tictoc-timer)\n[![Unit Testing](https://github.com/chrimaho/py-tictoc-timer/actions/workflows/unit-tests.yml/badge.svg?branch=main)](https://github.com/chrimaho/py-tictoc-timer/actions/workflows/unit-tests.yml)\n[![Publish Package](https://github.com/chrimaho/py-tictoc-timer/actions/workflows/pypi-publish.yml/badge.svg?branch=main)](https://github.com/chrimaho/py-tictoc-timer/actions/workflows/pypi-publish.yml)\n\nTime the execution of Python code using syntax similar to MATLAB\'s tic and toc functions.\n\n- [py-tictoc-timer](#py-tictoc-timer)\n  - [Installation](#installation)\n    - [Using `pip`:](#using-pip)\n    - [Using `pipenv`:](#using-pipenv)\n    - [Using `poetry`:](#using-poetry)\n    - [Using `conda`](#using-conda)\n  - [Usage](#usage)\n  - [Contribution](#contribution)\n  - [Build & Test](#build--test)\n    - [Run Black](#run-black)\n    - [Run PyTests:](#run-pytests)\n    - [Run MyPy Tests:](#run-mypy-tests)\n\n## Installation\n\n### Using [`pip`](https://pypi.org/project/pip):\n```sh\npip install py-tictoc-timer\n```\n\n### Using [`pipenv`](https://github.com/pypa/pipenv):\n```sh\npipenv install py-tictoc-timer\n```\n\n### Using [`poetry`](https://python-poetry.org):\n1. In your `pyproject.toml` file, add:\n    ```toml\n    [tool.poetry.dependencies]\n    py-tictoc-timer = "*"\n    ```\n2. Then in the terminal, run:\n    ```sh\n    poetry install\n    ```\n\n### Using [`conda`](https://docs.conda.io)\n```sh\nconda install py-tictoc-timer\n```\n\n## Usage\n\nBasic usage:\n```python linenums="1"\n>>> from tictoc import TicToc\n>>> from time import sleep\n>>> tt = TicToc()\n>>> tt.tic()\n>>> sleep(1.1)\n>>> tt.toc()\nElapsed time: 1secs\n```\n\nWithin context manager:\n```python linenums="1"\n>>> from tictoc import TicToc\n>>> from time import sleep\n>>> with TicToc():\n...     sleep(1.1)\nElapsed time: 1secs\n```\n\nWithin context manager using custom messages:\n```python linenums="1"\n>>> from tictoc import TicToc\n>>> from time import sleep\n>>> with TicToc(begin_message="start", end_message="end"):\n...     sleep(1.1)\nstart\nend: 1secs\n```\n\nCustom message:\n```python linenums="1"\n>>> from tictoc import TicToc\n>>> from time import sleep\n>>> with TicToc("Total Time"):\n...     sleep(1.1)\nTotal time: 1secs\n```\n\nWith restart during `.tic()`:\n```python linenums="1"\n>>> from tictoc import TicToc\n>>> from time import sleep\n>>> tt = TicToc()\n>>> tt.tic(restart=True)\n>>> sleep(1.1)\n>>> toc()\nElapsed time: 1secs\n>>> toc()\nElapsed time: 1secs\n```\n\nWith restart during `.toc()`:\n```python linenums="1"\n>>> from tictoc import TicToc\n>>> from time import sleep\n>>> tt = TicToc()\n>>> tt.tic()\n>>> sleep(1.1)\n>>> tt.toc(restart=True)\nElapsed time: 1secs\n>>> tt.toc()\nElapsed time: 1secs\n```\n\nWith restart using `.rtoc()`:\n```python linenums="1"\n>>> from tictoc import TicToc\n>>> from time import sleep\n>>> tt = TicToc()\n>>> tt.tic()\n>>> sleep(1.1)\n>>> tt.rtoc()\nElapsed time: 1secs\n>>> tt.toc()\nElapsed time: 1secs\n```\n\nWith time returned:\n```python linenums="1"\n>>> from tictoc import TicToc\n>>> from time import sleep\n>>> tt = TicToc()\n>>> tt.tic()\n>>> sleep(1.1)\n>>> value = tt.toc_value()\n>>> print(round(value, 1))\n1.1\n```\n\n## Contribution\nAll contributions are welcome!\n\n## Build & Test\n\n### Run [Black](https://black.readthedocs.io/)\n```sh\npython -m pipenv run python -m black --safe py_tictoc_timer tests\n```\n\n### Run [PyTests](https://docs.pytest.org):\n```sh\npython -m pipenv run python -m pytest --verbose --cov=py_tictoc_timer --cov-report=term --cov-report=html:cov-report/html --cov-report=xml:cov-report/xml/cov-report.xml\n```\n\n### Run [MyPy](http://www.mypy-lang.org) Tests:\n```sh\npipenv run mypy py_tictoc_timer --ignore-missing-imports --pretty --install-types --non-interactive\n```\n',
    'author': 'Chris Mahoney',
    'author_email': 'chrismahoney@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/chrimaho/py-tictoc-timer.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
