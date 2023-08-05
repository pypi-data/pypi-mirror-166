# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['secretscanner']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'rich>=12.5.1,<13.0.0']

setup_kwargs = {
    'name': 'secretscanner',
    'version': '0.1.0',
    'description': 'Scan for secrets within files.',
    'long_description': '# Secret Scanner\n\nA simple tool to scan directories for secrets using regular expressions.\n\n## Install\n\nInstall using either [`pip`](https://pypi.org/project/pip/), [`pipx`](https://pypi.org/project/pipx/) or your Python installer of choice\n\n```\npipx install secretscanner\n```\n\n## Usage\n\nTo scan a directory and print the files with secrets\n\n```\nsecretscanner DIRECTORY\n```\n\nTo also display info on the tokens that have been found pass the `-v`/`--verbose` flag.\n\nTo hide the output pass the `-q`/`--quiet` flag.\n\nIf secrets are found the tool exits with exit code `1`\n\n## Recognized Secrets\n\nThe tool currently recognizes the following secret types\n\n- Github access tokens\n- PyPI access tokens\n- Digital Ocean access tokens\n',
    'author': 'Simon Kennedy',
    'author_email': 'sffjunkie+code@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sffjunkie/secretscanner',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
