# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['confspawn']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=3.1.0,<4.0.0', 'tomli>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['confenv = confspawn.cli:config_value',
                     'confspawn = confspawn.cli:spawner']}

setup_kwargs = {
    'name': 'confspawn',
    'version': '0.2.0',
    'description': 'Easily build configuration files from templates.',
    'long_description': 'None',
    'author': 'Tip ten Brink',
    'author_email': '75669206+tiptenbrink@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
