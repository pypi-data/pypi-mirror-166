# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shipyard',
 'shipyard.api',
 'shipyard.api.v1',
 'shipyard.cli',
 'shipyard.colony',
 'shipyard.deploy',
 'shipyard.envoy',
 'shipyard.vigil']

package_data = \
{'': ['*']}

install_requires = \
['docker[ssh]>=5.0.3,<6.0.0',
 'fastapi>=0.79.0,<0.80.0',
 'typer[all]>=0.6.1,<0.7.0',
 'uvicorn[standard]>=0.18.2,<0.19.0']

entry_points = \
{'console_scripts': ['shipyard = shipyard.cli.main:app']}

setup_kwargs = {
    'name': 'shipyard-urbit',
    'version': '0.1.1',
    'description': 'Urbit hosting and automation platform',
    'long_description': '# Shipyard\n\nUrbit hosting and automation platform.\n\nNote: this is a Pre-Release package.  All changes will be breaking.  Wait for release 1.0.0 or later.\n\n## Install\n\n```\npip install shipyard-urbit\n```\n\n## Usage\n\n```\nshipyard\n```\n\n## API Overview\n\nVisit [redacted] for full API Documentation.\n\n## Development\n\n### Modules\n\n#### shipyard\n\n * `models.py` - types used throughout the project\n * `multi.py` - process management utilities\n\n#### shipyard.api\n\nHTTP API built with FastAPI.\n\n#### shipyard.cli\n\nCommand-line interface built with Typer.\n\n#### shipyard.colony\n\nHost setup and configuration using Ansible.\n\n#### shipyard.deploy\n\nCreating and migrating Urbit ships within our host infrastructure.\n\n#### shipyard.envoy\n\nCommunication and direction of Urbit ships.\n\n#### shipyard.vigil\n\nMonitoring and alerting. WIP.\n\n## License\n\nThis project is licensed under Apache-2.0.  Code licensed from other projects will be clearly marked with the appropriate notice.\n',
    'author': 'nodreb-borrus',
    'author_email': 'nodreb@borr.us',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
