# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pydiverse',
 'pydiverse.pipedag',
 'pydiverse.pipedag.backend',
 'pydiverse.pipedag.backend.table',
 'pydiverse.pipedag.backend.table.util',
 'pydiverse.pipedag.context',
 'pydiverse.pipedag.core',
 'pydiverse.pipedag.engine',
 'pydiverse.pipedag.errors',
 'pydiverse.pipedag.materialize',
 'pydiverse.pipedag.materialize.util',
 'pydiverse.pipedag.util']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.39,<2.0.0',
 'attrs>=22.1.0,<23.0.0',
 'msgpack>=1.0.4,<2.0.0',
 'networkx>=2.8.5,<3.0.0',
 'packaging>=21.3,<22.0',
 'pandas>=1.4.3,<2.0.0',
 'prefect>=1.3,<3',
 'pynng>=0.7.1,<0.8.0',
 'structlog>=22.1.0,<23.0.0',
 'tomli>=2.0.1,<3.0.0',
 'typing-extensions>=4.1.0,<5']

extras_require = \
{'docs': ['Sphinx>=5.1.1,<6.0.0',
          'sphinx-rtd-theme>=1.0.0,<2.0.0',
          'sphinxcontrib-apidoc>=0.3.0,<0.4.0'],
 'filelock': ['filelock>=3.7.1,<4.0.0'],
 'zookeeper': ['kazoo>=2.8.0,<3.0.0']}

setup_kwargs = {
    'name': 'pydiverse-pipedag',
    'version': '0.1.0',
    'description': 'A pipeline orchestration layer built on top of prefect for caching and cache invalidation to SQL and blob store targets.',
    'long_description': '# pydiverse.pipedag\n\n[![CI](https://github.com/pydiverse/pydiverse.pipedag/actions/workflows/ci.yml/badge.svg)](https://github.com/pydiverse/pydiverse.pipedag/actions/workflows/ci.yml)\n\nA pipeline orchestration layer built on top of prefect for caching and cache invalidation to SQL and blob store targets.\n\n## Preparing installation\n\nTo install the package locally in development mode, you first have to install\n[Poetry](https://python-poetry.org/docs/#installation).\n\nWhen installing poetry using conda(I know this sounds odd), it is recommended to install\nalso compilers, so source packages can be built on `poetry install`. Since we use psycopg2,\nit also helps to install psycopg2 in conda to have pg_config available:\n\n```bash\nconda install -n poetry -c poetry conda-forge compilers cmake make psycopg2\nconda activate poetry  # only needed for poetry install\n```\n\nOn OSX, a way to install pg_config (needed for source building psycopg2 by `poetry install`) is\n\n```bash\nbrew install postgresql\n```\n\n## Installation\n\n> Currently, development on pipedag is not possible with Windows. The current setup of installing prefect and running\n> tests with docker (to spin up Postgres and Zookeeper) fail in poetry dependency resolution. It would be a nice\n> contribution to find drop-in replacements for both that run as simple python dependency without docker and moving\n> docker based tests to github actions (multi-DB target tests will be moved to cloud anyways).\n\nAfter that, install pydiverse pipedag like this:\n\n```bash\ngit clone https://github.com/pydiverse/pydiverse.pipedag.git\ncd pydiverse.pipedag\n\n# Create the environment, activate it and install the pre-commit hooks\npoetry install\npoetry shell\npre-commit install\n```\n\n## Pre-commit install with conda and python 3.8\n\nWe currently have some pre-commit hooks bound to python=3.8. So pre-commit install may fail when running with\npython=3.10 python environment. However, the pre-commit environment does not need to be the same as the environment\nused for testing pipedag code. When using conda, you may try:\n\n```bash\nconda install -n python38 -c python=3.8 pre_commit\nconda activate python38\npre-commit install\n```\n\n## Testing\n\nTo facilitate easy testing, we provide a Docker Compose file to start all required servers.\nJust run `docker compose up` in the root directory of the project to start everything, and then run `pytest` in a new\ntab.\n\nYou can inspect the contents of the PipeDAT Postgres database at `postgresql://postgres:pipedag@127.0.0.1/pipedag`.\nTo reset the state of the docker containers you can run `docker compose down`.\nThis might be necessary if the database cache gets corrupted.\n',
    'author': 'QuantCo, Inc.',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
