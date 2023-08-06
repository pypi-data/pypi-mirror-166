# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mait_manager']

package_data = \
{'': ['*']}

install_requires = \
['alive-progress>=2.4.1,<3.0.0', 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['mait = mait_manager.main:app']}

setup_kwargs = {
    'name': 'mait-manager',
    'version': '0.1.4',
    'description': 'Package manager for text adventure games.',
    'long_description': '# mait: package manager for text adventure games.\n[![test-mait.gif](https://i.postimg.cc/XYYy4Xpp/test-mait.gif)](https://postimg.cc/F7wKxrb4)\n\n### Installing is by the PIP manager [Linux]\n```commandline\npip3 install mait-manager\n```\n### Similar for [Windows]\n```commandline\npy -m pip install mait-manager\n```\n***You invoke mait via CLI by using the following:***\n```commandline\nmait --help\n```\n\n# uploading.\n[![upload-mait.gif](https://i.postimg.cc/BvKq5Gjq/upload-mait.gif)](https://postimg.cc/B8J9sk5y)\nThe above demonstrates how to upload a single file **(You cannot upload multiple files at this time.)**\n### Uploading.\n```commandline\nmait upload\n```\nCode must be source code! Compiled sources are not allowed!\n### Providing a JSON.\n```json\n{\n  "exec": "python3 donut.py"\n}\n```\nA JSON provides the command to compile/or interpret the code & is required.\n\n**Uploading requires for the file to be reviewed since malicious code can easily be run.** \nAllow up to 48 hours for me to review (I\'m a one-man band y\'know). If you think the review process is \nbeing prolonged, contact me at `saynemarsh9@gmail.com`\n',
    'author': 'Zayne Marsh',
    'author_email': 'saynemarsh9@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
