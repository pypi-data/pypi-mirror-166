# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azcam_archon']

package_data = \
{'': ['*']}

install_requires = \
['azcam']

setup_kwargs = {
    'name': 'azcam-archon',
    'version': '22.3',
    'description': 'Azcam extension for Semiconductor Technology Associates (STA) Archon controllers',
    'long_description': '# azcam-archon\n\n*azcam-archon* is an *azcam* extension for STA Archon controllers. See http://www.sta-inc.net/archon/.\n\n## Installation\n\n`pip install azcam-archon`\n\nOr download from github: https://github.com/mplesser/azcam-archon.git.\n\n## Example Code\n\nThe code below is for example only.\n\n### Controller\n```python\nimport azcam.server\nfrom azcam_archon.controller_archon import ControllerArchon\ncontroller = ControllerArchon()\ncontroller.camserver.port = 4242\ncontroller.camserver.host = "10.0.2.10"\ncontroller.header.set_keyword("DEWAR", "ITL1", "Dewar name")\ncontroller.timing_file = os.path.join(\n    azcam.db.systemfolder, "archon_code", "ITL1_STA3800C_Master.acf"\n)\n```\n\n### Exposure\n```python\nimport azcam.server\nfrom azcam_archon.exposure_archon import ExposureArchon\nexposure = ExposureArchon()\nfiletype = "MEF"\nexposure.fileconverter.set_detector_config(detector_sta3800)\nexposure.filetype = azcam.db.filetypes[filetype]\nexposure.image.filetype = azcam.db.filetypes[filetype]\nexposure.display_image = 1\nexposure.image.remote_imageserver_flag = 0\nexposure.add_extensions = 1\n```\n',
    'author': 'Michael Lesser',
    'author_email': 'mlesser@arizona.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mplesser/azcam-archon/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
