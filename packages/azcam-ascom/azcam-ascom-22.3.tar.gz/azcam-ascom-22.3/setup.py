# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azcam_ascom']

package_data = \
{'': ['*']}

install_requires = \
['azcam', 'pywin32>=304,<305']

setup_kwargs = {
    'name': 'azcam-ascom',
    'version': '22.3',
    'description': 'Azcam extension for ASCOM cameras',
    'long_description': '# azcam-ascom\n\n*azcam-ascom* is an *azcam* extension for ASCOM cameras. See https://ascom-standards.org/.\n\nThis code has been used for the QHY and ZWO cameras.\n\n## Installation\n\n`pip install azcam-ascom`\n\nOr download from github: https://github.com/mplesser/azcam-ascom.git.\n\n## Example Code\n\nThe code below is for example only.\n\n### Controller\n\n```python\nimport azcam.server\nfrom azcam_ascom.controller_ascom import ControllerASCOM\ncontroller = ControllerASCOM()\n```\n\n### Exposure\n\n```python\nimport azcam.server\nfrom azcam_ascom.exposure_ascom import ExposureASCOM\nexposure = ExposureASCOM()\nfiletype = "FITS"\nexposure.filetype = exposure.filetypes[filetype]\nexposure.image.filetype = exposure.filetypes[filetype]\nexposure.display_image = 1\nexposure.image.remote_imageserver_flag = 0\nexposure.set_filename("/data/zwo/asi1294/image.fits")\nexposure.display_image = 1\n```\n',
    'author': 'Michael Lesser',
    'author_email': 'mlesser@arizona.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mplesser/azcam-ascom/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
