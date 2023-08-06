# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitbook_dl']

package_data = \
{'': ['*']}

install_requires = \
['pypandoc>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'gitbook-dl',
    'version': '0.2.0',
    'description': 'gitbook-dl',
    'long_description': '# gitbook-dl\n\nCommand-line program to download books from gitbook.com\n\n:warning: _This package is currently under development_\n\n## Purpose\n\n## Get Started\n\n### Installing\n\nThe easiest way to install `gitbook-dl` is via `pip`:\n\n```console\npip install gitbook-dl\n```\n\n## Contributing\n\n### Developer Guide\n\n1. Clone this repository `git clone git@github.com:alwinw/gitbook-dl.git`\n2. Install the development version `pip install -v -e .[<extras>]` (`-e` needs pip >= 22.0 for pyproject.toml) or `poetry install --extras "<extras>"`\n3. Make your changes and commit using [commitizen](https://commitizen-tools.github.io/commitizen/#installation) and ensure [pre-commit](https://pre-commit.com/#install) is active\n4. When bumping version, use `cz bump -ch -cc`\n5. When ready, bump the version and run `poetry build -v`. If deploying, run `poetry publish --build -v`\n',
    'author': 'alwinw',
    'author_email': '16846521+alwinw@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alwinw/gitbook-dl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
