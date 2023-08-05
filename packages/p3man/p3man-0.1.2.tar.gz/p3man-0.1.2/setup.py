# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['p3man']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'cryptography>=37.0.4,<38.0.0']

entry_points = \
{'console_scripts': ['p3man = p3man:cli']}

setup_kwargs = {
    'name': 'p3man',
    'version': '0.1.2',
    'description': 'Password manager. Manage your passwords as simple as 1, 2, 3',
    'long_description': "# p3man\nThe password manager as simple as 1, 2, 3\n\n### Keep. It. Simple. Secure. (KISS)\n\n```\nUsage: p3man [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  add     Add (username) and (password) for an account\n  get     Retrieves password from account.\n  list    List accounts in database (hashed).\n  remove  Remove an account\n  reset   Reset your master password.\n  setup   Setup up your account and master password\n  update  Update password for an account.\n  wipe    Removes all data, all passwords from device (irreversable)\n```\n\n### Security\n\nYour master password is hashed via python's cryptography's Scrypt.\nYour accounts encrypted using the <em>original</em> password.\n![](workflow.png)\n\n\n",
    'author': 'curtis',
    'author_email': 'curtis.hu688@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/curtisjhu/p3man',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
