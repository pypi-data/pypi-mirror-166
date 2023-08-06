# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azcam_webtools',
 'azcam_webtools.exptool',
 'azcam_webtools.status',
 'azcam_webtools.status.tests']

package_data = \
{'': ['*'],
 'azcam_webtools.exptool': ['code/*'],
 'azcam_webtools.status': ['code/*']}

install_requires = \
['azcam', 'fastapi', 'jinja2']

setup_kwargs = {
    'name': 'azcam-webtools',
    'version': '22.3',
    'description': 'Azcam extension which implements various browser-based tools',
    'long_description': '# azcam-webtools\n\n*azcam-webtools* is an *azcam* extension which implements various browser-based tools.\n\n## Installation\n\n`pip install azcam-webtools`\n\nOr download from github: https://github.com/mplesser/azcam-webtools.git.\n\n## Usage\n\nOpen a web browser to http://localhost:2403/XXX where XXX is a toolname, with the appropriate replacements for localhost and the web server port number.\n\n## Tools\n - status - display current exposure status\n - exptool - a simple exposure control tool\n',
    'author': 'Michael Lesser',
    'author_email': 'mlesser@arizona.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mplesser/azcam-webtools/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
