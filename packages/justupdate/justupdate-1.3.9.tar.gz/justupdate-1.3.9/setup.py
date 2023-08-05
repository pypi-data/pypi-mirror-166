# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['justupdate',
 'justupdate.cli',
 'justupdate.client',
 'justupdate.core',
 'justupdate.repo']

package_data = \
{'': ['*'],
 'justupdate': ['templates/*',
                'templates/MAC/*',
                'templates/MAC/scripts/*',
                'templates/win/*']}

install_requires = \
['appdirs>=1.4,<2.0',
 'paramiko>=2.7,<3.0',
 'pyinstaller>=4.1,<5.0',
 'requests-cache>=0.5,<0.6',
 'requests>=2,<3',
 'scp>=0.13,<0.14']

entry_points = \
{'console_scripts': ['justupdate = justupdate.cli:main']}

setup_kwargs = {
    'name': 'justupdate',
    'version': '1.3.9',
    'description': '',
    'long_description': "# Just. Update\n\n[![Build Status](https://travis-ci.com/JessicaTegner/JustUpdate.svg?branch=master)](https://travis-ci.com/JessicaTegner/JustUpdate)\n\nJust. Update is a updater system written in python that utilizes each platform's native method of installing an application to perform an update.\n* On windows, JustUpdate uses NSIS (nullsoft scriptable install system) to perform the update.\n* On Mac, JustUpdate uses the pkg flat installer archive format, to perform the update (productbuild).\n\n# [INSTALLATION](https://JessicaTegner.github.io/JustUpdate#installation) | [DOCUMENTATION](https://JessicaTegner.github.io/JustUpdate#usage) | [LICENSE](https://github.com/JessicaTegner/JustUpdate/blob/master/license) | [HELPING OUT](https://JessicaTegner.github.io/JustUpdate/#helping-out)\n\n### Contributing\nWant a feature or found a bug? Open an issue or submit a pull request.\n",
    'author': 'JessicaTegner',
    'author_email': 'jessica.tegner@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JessicaTegner/JustUpdate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
