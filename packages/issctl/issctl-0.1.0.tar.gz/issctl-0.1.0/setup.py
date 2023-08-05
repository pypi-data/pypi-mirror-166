# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['issctl', 'issctl.lib']

package_data = \
{'': ['*']}

install_requires = \
['fire==0.4.0', 'pydantic==1.10.1', 'python-magic==0.4.24', 'rich==12.5.1']

entry_points = \
{'console_scripts': ['issctl = issctl.main:run']}

setup_kwargs = {
    'name': 'issctl',
    'version': '0.1.0',
    'description': 'Tools for automated issues management',
    'long_description': '# issctl\n\nIssue Manager CLI tool.\n\n- Tool to automate your development process\n- Heavily inspired by [PDD](https://www.yegor256.com/2017/04/05/pdd-in-action.html) concept\n',
    'author': 'Kirill K',
    'author_email': 'kovalev.kirill.a@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
