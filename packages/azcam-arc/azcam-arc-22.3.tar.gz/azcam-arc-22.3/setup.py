# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azcam_arc']

package_data = \
{'': ['*']}

install_requires = \
['azcam']

setup_kwargs = {
    'name': 'azcam-arc',
    'version': '22.3',
    'description': 'Azcam extension for Astronomical Research Cameras (ARC) gen1, gen2, and gen3 controllers',
    'long_description': '# azcam-arc\n\n*azcam-arc* is an *azcam* extension for Astronomical Research Cameras, Inc. gen1, gen2, and gen3 controllers. See https://www.astro-cam.com/.\n\n## Installation\n\n`pip install azcam-arc`\n\nOr download from github: https://github.com/mplesser/azcam-arc.git.\n\n## Example Code\n\nThe code below is for example only.\n\n### Controller Setup\n```python\nimport azcam.server\nfrom azcam_arc.controller_arc import ControllerArc\ncontroller = ControllerArc()\ncontroller.timing_board = "arc22"\ncontroller.clock_boards = ["arc32"]\ncontroller.video_boards = ["arc45", "arc45"]\ncontroller.utility_board = None\ncontroller.set_boards()\ncontroller.pci_file = os.path.join(azcam.db.systemfolder, "dspcode", "dsppci3", "pci3.lod")\ncontroller.video_gain = 2\ncontroller.video_speed = 1\n```\n\n### Exposure Setup\n```python\nimport azcam.server\nfrom azcam_arc.exposure_arc import ExposureArc\nexposure = ExposureArc()\nexposure.filetype = azcam.db.filetypes["MEF"]\nexposure.image.filetype = azcam.db.filetypes["MEF"]\nexposure.set_remote_imageserver("localhost", 6543)\nexposure.image.remote_imageserver_filename = "/data/image.fits"\nexposure.image.server_type = "azcam"\nexposure.set_remote_imageserver()\n```\n\n## Camera Servers\n*Camera servers* are separate executable programs which manage direct interaction with \ncontroller hardware on some systems. Communication with a camera server takes place over a socket via \ncommunication protocols defined between *azcam* and a specific camera server program. These \ncamera servers are necessary when specialized drivers for the camera hardware are required.  They are \nusually written in C/C++. \n\n## DSP Code\nThe DSP code which runs in the ARC controllers is assembled and linked with\nMotorola software tools. These tools are typically installed in the folder `/azcam/motoroladsptools/` on a\nWindows machine as required by the batch files which assemble and link the code.\n\nWhile the AzCam application code for the ARC timing board is typically downloaded during\ncamera initialization, the boot code must be compatible for this to work properly. Therefore\nAzCam-compatible DSP boot code may need to be burned into the timing board EEPROMs before use, depending on configuration. \n\nThe gen3 PCI fiber optic interface boards and the gen3 utility boards use the original ARC code and do not need to be changed. The gen1 and gen2 situations are more complex.\n\nFor ARC system, the *xxx.lod* files are downlowded to the boards.\n',
    'author': 'Michael Lesser',
    'author_email': 'mlesser@arizona.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mplesser/azcam-arc/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
