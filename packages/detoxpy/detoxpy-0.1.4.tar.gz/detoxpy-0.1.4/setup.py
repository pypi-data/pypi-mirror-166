# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['detoxpy']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['detox = detoxpy:cli.main', 'detoxpy = detoxpy:cli.main']}

setup_kwargs = {
    'name': 'detoxpy',
    'version': '0.1.4',
    'description': 'A tool to rename directories/files that contain unsafe characters',
    'long_description': "# detox\n\n`detox` is a Python tool that can be used to rename directories/files with unsafe characters or spaces[^1].\n\n[![Supported Python versions](https://img.shields.io/badge/Python-%3E=3.6-blue.svg?logo=python)](https://www.python.org/downloads/) [![PEP8](https://img.shields.io/badge/Code%20style-PEP%208-orange.svg?logo=python)](https://www.python.org/dev/peps/pep-0008/) \n [![Poetry-build](https://github.com/Alyetama/detox/actions/workflows/poetry-build.yml/badge.svg)](https://github.com/Alyetama/detox/actions/workflows/poetry-build.yml)\n\n## Requirements\n\n- [Python>=3.6](https://www.python.org/downloads/)\n\n## Installation\n\n```shell\npip install -U detoxpy\n```\n\n## Usage\n\n```\nusage: detox [-h] [-r] [-R REPLACE_WITH] [-t] [-l] [-n] [-p] path [path ...]\n\npositional arguments:\n  path                  Path to a single or multiple files/directories to detox\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -r, --recursive       Rename files recursively\n  -R REPLACE_WITH, --replace-with REPLACE_WITH\n                        Replace spaces and unsafe characters with this character (default: '_')\n  -t, --keep-trailing   Keep the trailing character if exists (e.g., 'foo_')\n  -l, --keep-leading    Keep the leading character if exists (e.g., '_foo')\n  -n, --dry-run         Do a trial run with no permanent changes\n  -p, --plain-print     Print the change as plain text\n```\n\n## Examples\n\n### Example 1: Detox a single file/directory:\n\n```shell\ndetox '(foo)^bar.txt'\n# '(foo)^bar.txt' --> 'foo_bar.txt'\n\ndetox 'foo&bar/'\n# 'foo&bar' --> 'foo_bar'\n```\n\n### Example 2: Detox a directory recursively:\n\n```shell\n# foo bar\n# └── foo1&foo2\n#     ├── foo bar (copy 1).jpg\n#     └── foo bar (copy 2).jpg\n\ndetox -r 'foo bar'\n\n# foo_bar\n# └── foo1_foo2\n#     ├── foo_bar_copy_1.jpg\n#     └── foo_bar_copy_2.jpg\n```\n\n### Example 3: Duplicate names after detoxing\n\n- `detox` will avoid overwriting if the detoxed name already exists. For example:\n\n```shell\ntree 'foo foo'\n# foo foo\n#   ├── foo^bar.jpg\n#   └── foo%bar.jpg\n\ndetox -r -i 'foo foo'\n\n# foo_foo\n#   ├── foo_bar.jpg\n#   └── foo_bar-1.jpg\n```\n\n[^1]: The name `detox` is inspired by the tool [detox](https://linux.die.net/man/1/detox).\n",
    'author': 'Alyetama',
    'author_email': 'malyetama@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
