# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azcam_monitor', 'azcam_monitor.webserver']

package_data = \
{'': ['*'],
 'azcam_monitor.webserver': ['static/*',
                             'static/bootstrap/css/*',
                             'static/bootstrap/js/*']}

install_requires = \
['azcam', 'fastapi', 'psutil', 'uvicorn']

setup_kwargs = {
    'name': 'azcam-monitor',
    'version': '22.3',
    'description': 'Azcam monitoring application',
    'long_description': '# azcam-monitor\n\n*azcam-monitor* is an *azcam* extension app used to monitor and control *azcam* processes on the local network.\n\n## Installation\n\n`pip install azcam-monitor`\n\nOr download from github: https://github.com/mplesser/azcam-monitor.git.\n\n## Startup and configuration\n\nRun the app from its folder, it is not a python package.\n\nExample:\n\n``azcammonitor.py -configfile \\somefolder\\parameters_monitor_example.ini``\n\n## Credits\n\nOrginally written by Grzegorz Zareba.\n\nMaintained by Michael Lesser.\n',
    'author': 'Michael Lesser',
    'author_email': 'mlesser@arizona.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mplesser/azcam-monitor/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
