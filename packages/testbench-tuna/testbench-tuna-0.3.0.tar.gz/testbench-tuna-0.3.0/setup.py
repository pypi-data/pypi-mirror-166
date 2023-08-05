# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['testbench_tuna']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.81.0,<0.82.0',
 'requests>=2.28.1,<3.0.0',
 'uvicorn>=0.18.2,<0.19.0']

setup_kwargs = {
    'name': 'testbench-tuna',
    'version': '0.3.0',
    'description': 'Personal testbench for trying out stuff',
    'long_description': '# Testbench Tuna\n\n[![pypi package](https://badge.fury.io/py/testbench-tuna.svg)](https://pypi.python.org/pypi/testbench-tuna/)\n[![python](https://img.shields.io/pypi/pyversions/testbench-tuna.svg)](https://pypi.python.org/pypi/testbench-tuna)\n[![downloads](https://pepy.tech/badge/testbench-tuna)](https://pepy.tech/project/testbench-tuna)\n[![codecov](https://codecov.io/gh/trallnag/testbench-tuna/branch/trunk/graph/badge.svg?token=400YFJSVG7)](https://codecov.io/gh/trallnag/testbench-tuna)\n\nPersonal testbench where I try out things.\n\n- Python app, not meant to be used as a library.\n- Web application using [FastAPI](https://fastapi.tiangolo.com/)\n- For testing [pytest](https://docs.pytest.org/) is used.\n- Release Management with\n  [Release Please](https://github.com/googleapis/release-please). Focused on\n  simple manual release process with the option add custom info to a release and\n  the changelog before performing a release. Balance between full automation\n  with something like semantic-release and manual release creation via the\n  GitHub UI.\n- Pre-commit stuff. Code coverage with CodeCov. Poetry.\n- ...\n\nRandom links and references:\n\n- <https://github.com/google-github-actions/release-please-action>\n- <https://github.com/googleapis/release-please>\n',
    'author': 'Tim Schwenke',
    'author_email': 'tim.schwenke@trallnag.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/trallnag/testbench-tuna',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
