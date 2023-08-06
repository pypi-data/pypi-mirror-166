# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azcam_scripts']

package_data = \
{'': ['*']}

install_requires = \
['astropy', 'azcam', 'matplotlib', 'numpy', 'requests', 'scipy']

setup_kwargs = {
    'name': 'azcam-scripts',
    'version': '22.3',
    'description': 'Azcam extension which adds general purpose scripts',
    'long_description': '# azcam-scripts\n\n*azcam-scripts* is an *azcam* extension which adds general purpose scripting. These scripts are intended for command line use. Other azcam extensions may required to be installed for proper operation, depending on the script.\n\n## Installation\n\n`pip install azcam-scripts`\n\nOr download from github: https://github.com/mplesser/azcam-scripts.git.\n\n## Usage\n\nUse `from azcam_scripts import xxx` to import module `xxx`. Scripts may then be executed by name as `xxx.xxx(10)`, for example, `get_temperatures.get_temperatures(10)`. A shortcut could be similar to `from azcam_scripts.get_temperatures import get_temperatures` and then execute with `get_temperatures(10)`.\n\nIn some cases the environment configuration process may bring all the script functions directly to the command line namespace. This is usually accomplished using the `azcam_scripts.load()` command.  In this case, use just `get_temperaturess(10, "templog.txt", 0)`.\n',
    'author': 'Michael Lesser',
    'author_email': 'mlesser@arizona.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mplesser/azcam-scripts/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
