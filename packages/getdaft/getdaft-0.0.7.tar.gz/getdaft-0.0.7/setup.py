# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daft',
 'daft.execution',
 'daft.experimental',
 'daft.experimental.datarepo',
 'daft.experimental.serving',
 'daft.experimental.serving.backends',
 'daft.experimental.serving.static',
 'daft.internal',
 'daft.logical',
 'daft.runners']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1.0,<10.0.0',
 'fsspec',
 'loguru>=0.6.0,<0.7.0',
 'numpy>=1.16.6,<2.0.0',
 'pandas>=1.3.5,<2.0.0',
 'protobuf>=3.19.0,<3.20.0',
 'pyarrow>=8.0.0,<9.0.0',
 'pydantic[dotenv]>=1.9.1,<2.0.0',
 'pydot>=1.4.2,<2.0.0',
 'ray==1.13.0',
 'tabulate>=0.8.10,<0.9.0']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=3.8.0,<4.0.0'],
 'experimental': ['fastapi>=0.79.0,<0.80.0',
                  'docker>=5.0.3,<6.0.0',
                  'uvicorn>=0.18.2,<0.19.0',
                  'cloudpickle>=2.1.0,<3.0.0',
                  'boto3>=1.23.0,<2.0.0',
                  'PyYAML>=6.0,<7.0',
                  'icebridge==0.0.3'],
 'iceberg': ['icebridge==0.0.3'],
 'serving': ['fastapi>=0.79.0,<0.80.0',
             'docker>=5.0.3,<6.0.0',
             'uvicorn>=0.18.2,<0.19.0',
             'cloudpickle>=2.1.0,<3.0.0',
             'boto3>=1.23.0,<2.0.0',
             'PyYAML>=6.0,<7.0']}

entry_points = \
{'console_scripts': ['build_inplace = build:build_inplace']}

setup_kwargs = {
    'name': 'getdaft',
    'version': '0.0.7',
    'description': 'A Distributed DataFrame library for large scale complex data processing.',
    'long_description': '# Developing on Daft\n\n1. [Install Poetry](https://python-poetry.org/docs/#installation)\n2. Init your python environment\n    - `poetry install`\n3. Build Extensions locally\n    - `poetry run build_inplace`\n4. Run tests\n    - `poetry run pytest`\n5. Run type checking\n    - `poetry run mypy`\n6. Run any other script\n    - `poetry run CMD`\n7. Add package\n    - `poetry add PACKAGE`\n8. Lock env\n    - `poetry lock`\n',
    'author': 'Eventual Inc',
    'author_email': 'daft@eventualcomputing.com',
    'maintainer': 'Sammy Sidhu',
    'maintainer_email': 'sammy@eventualcomputing.com',
    'url': 'https://getdaft.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
