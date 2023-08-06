# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tapi', 'tapi.api', 'tapi.cli', 'tapi.cli.run']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'fastapi>=0.82.0,<0.83.0',
 'rich>=12.5.1,<13.0.0',
 'typer>=0.6.1,<0.7.0',
 'uvicorn>=0.18.3,<0.19.0']

setup_kwargs = {
    'name': 'pytapi',
    'version': '0.1.0',
    'description': 'Python no-code API framework. Create REST interfaces from YAML configs',
    'long_description': None,
    'author': 'PSauerborn',
    'author_email': 'pascal.sauerborn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
