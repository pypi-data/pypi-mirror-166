# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipl_config']

package_data = \
{'': ['*']}

install_requires = \
['ipapp[fastapi,postgres]>=1.3.9,<2.0.0', 'uvloop>=0.16.0,<0.17.0']

extras_require = \
{'dotenv': ['python-dotenv>=0.21.0,<0.22.0'],
 'hcl2': ['python-hcl2>=3.0.5,<4.0.0'],
 'toml': ['toml>=0.10.2,<0.11.0'],
 'yaml': ['pyyaml>=5.4,<6.0']}

setup_kwargs = {
    'name': 'ipl-config',
    'version': '0.1.2',
    'description': 'InPlat config adapters',
    'long_description': '[![tests](https://github.com/koi8-r/ipl-config/actions/workflows/ci.yml/badge.svg)](https://github.com/koi8-r/ipl-config/actions/workflows/ci.yml)\n[![codecov](https://codecov.io/gh/koi8-r/ipl-config/branch/master/graph/badge.svg?token=OKURU75Y7A)](https://codecov.io/gh/koi8-r/ipl-config)\n[![pypi](https://img.shields.io/pypi/v/ipl-config.svg)](https://pypi.python.org/pypi/ipl-config)\n[![versions](https://img.shields.io/pypi/pyversions/ipl-config.svg)](https://github.com/koi8-r/ipl-config)\n\n\n# Config adapters with pydantic behavior\n- json\n- yaml\n- toml\n- hcl2\n- environ\n- .env\n\n## Examples\n- [yaml config with env, dotenv and args overrides](/examples/config_yaml_dump.py)\n',
    'author': 'InPlat',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/koi8-r/ipl-config',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
