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
    'version': '0.0.4',
    'description': 'Future Agile CICD tooling template',
    'long_description': '# agileetc\n\nExample python 3.9+ project where we can develop best practices and provide teams with a useful template.\n\n## Prerequisites\n\nThis project uses poetry is a tool for dependency management and packaging in Python. It allows you to declare the \nlibraries your project depends on, it will manage (install/update) them for you. Use the installer rather than pip:\n\n[installing-with-the-official-installer](https://python-poetry.org/docs/master/#installing-with-the-official-installer).\n\n```sh\npoetry self add poetry-bumpversion\n```\n\n```sh\npoetry -V\nPoetry (version 1.2.0)\n```\n\n## Features\n\n1. Poetry packaged python project with example CLI entry point.\n2. Linux and Windows compatible project.\n3. Example read/write YML files.\n4. Example Unit Tests.\n5. Example flake8 linter configuration.\n6. Example line operation via click API allowing project to be ran from command line of from CICD pipelines.\n7. Example use of Fabric API to execute external commands.\n8. Example use of Texttable for pretty table output.\n9. Example Jenkins pipeline.\n10. Example GitHub actions. \n11. 11Python package publishing to PiPy. \n12. Docker image publishing to docker hub. \n13. Example usage of python package. \n14. Example usage of docker image.\n\n## Getting Started\n\n```sh\npoetry update\n```\n\n```sh\npoetry install\n```\n\n## Run\n```sh\npoetry run agileetc\n```\n\n## Lint\n```sh\npoetry run flake8\n```\n\n## Test\n```sh\npoetry run pytest\n```\n\n## Publish\n\n* By default we are using [PYPI packages](https://packaging.python.org/en/latest/tutorials/installing-packages/). \n* Create yourself an access token for PYPI and then follow the instructions.\n\n```sh\nexport PYPI_USERNAME=__token__ \nexport PYPI_PASSWORD=<Your API Token>\npoetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD\n```\nThe build option will automatically build the release artifacts for you as shown below.\n\n![](../../docs/images/Screenshot at 2022-09-10 10-41-06.png)\n\nYou can then verify that your newly released package has been published.\n\n![](../../docs/images/Screenshot at 2022-09-10 11-16-41.png)\n\n## Versioning\nWe use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/Agile-Solutions-GB-Ltd/agileup/tags). \n\n## Releasing\n\nWe are using [poetry-bumpversion](https://github.com/monim67/poetry-bumpversion) to manage release versions.\n\n```sh\npoetry version patch\n```\n\n## Dependency\n\nOnce the release has been created it is now available for you to use in other python projects via:\n\n```sh\npip install agileetc\n```\n\nAnd also for poetry projects via:\n\n```sh\npoetry add aigleetc\n```\n\n## Contributing\n\nPlease read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.\n\n## License\n\nThis project is licensed under the Apache License, Version 2.0 - see the [LICENSE](LICENSE) file for details\n\n\n\n',
    'author': 'agileturret',
    'author_email': 'Paul.Gilligan@agilesolutions.co.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Agile-Solutions-GB-Ltd/automatic-eureka/tree/main/python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
