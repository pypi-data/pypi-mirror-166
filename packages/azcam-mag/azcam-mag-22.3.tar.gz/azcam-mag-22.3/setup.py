# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azcam_mag']

package_data = \
{'': ['*']}

install_requires = \
['azcam']

setup_kwargs = {
    'name': 'azcam-mag',
    'version': '22.3',
    'description': 'Azcam extension for OCIW Magellan ITL camera controllers',
    'long_description': '# azcam-mag\n\n*azcam-mag* is an *azcam* extension for OCIW Magellan CCD controllers (ITL version). See http://instrumentation.obs.carnegiescience.edu/ccd/gcam.html.\n\n## Installation\n\n`pip install azcam-mag`\n\nOr download from github: https://github.com/mplesser/azcam-mag.git.\n\n## Example Code\n\nThe code below is for example only.\n\n### Controller\n\n```python\nimport azcam.server\nfrom azcam_mag.controller_mag import ControllerMag\ncontroller = ControllerMag()\ncontroller.camserver.set_server("some_machine", 2402)\ncontroller.timing_file = os.path.join(azcam.db.datafolder, "dspcode/gcam_ccd57.s")\n```\n### Exposure\n\n```python\nimport azcam.server\nfrom azcam_mag.exposure_mag import ExposureMag\nexposure = ExposureMag()\nfiletype = "BIN"\nexposure.filetype = exposure.filetypes[filetype]\nexposure.image.filetype = exposure.filetypes[filetype]\nexposure.display_image = 1\nexposure.image.remote_imageserver_flag = 0\nexposure.set_filename("/azcam/soguider/image.bin")\nexposure.test_image = 0\nexposure.root = "image"\nexposure.display_image = 0\nexposure.image.make_lockfile = 1\n```\n\n## Camera Servers\n\n*Camera servers* are separate executable programs which manage direct interaction with controller hardware on some systems. Communication with a camera server takes place over a socket via communication protocols defined between *azcam* and a specific camera server program. These camera servers are necessary when specialized drivers for the camera hardware are required.  They are usually written in C/C++. \n\n## DSP Code\n\nThe DSP code which runs in Magellan controllers is assembled and linked with\nMotorola software tools. These tools should be installed in the folder `/azcam/motoroladsptools/` on Windows machines, as required by the batch files which assemble and link the code.\n\nFor Magellan systems, there is only one DSP file which is downloaded during initialization. \n\nNote that *xxx.s* files are loaded for the Magellan systems.\n',
    'author': 'Michael Lesser',
    'author_email': 'mlesser@arizona.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mplesser/azcam-mag/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
