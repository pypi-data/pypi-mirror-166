# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['agileetc']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'click>=8.1,<9.0', 'pytest>=7.1.3,<8.0.0']

entry_points = \
{'console_scripts': ['agileetc = agileetc.cli:cli']}

setup_kwargs = {
    'name': 'agileetc',
    'version': '0.0.1',
    'description': 'Future Agile CICD tooling',
    'long_description': 'None',
    'author': 'agileturret',
    'author_email': 'Paul.Gilligan@agilesolutions.co.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
