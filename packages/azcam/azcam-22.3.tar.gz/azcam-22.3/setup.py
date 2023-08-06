# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azcam', 'azcam.functions', 'azcam.tools']

package_data = \
{'': ['*']}

install_requires = \
['astropy', 'loguru', 'matplotlib', 'numpy']

setup_kwargs = {
    'name': 'azcam',
    'version': '22.3',
    'description': 'Acquisition and analysis package for scientific imaging',
    'long_description': '# AzCam\n\n*azcam* is an python package used to control an observation from a scientific imaging camera. It is intended to be used as an interface to multiple non-standard hardware interfaces such as camera controllers, telescopes, instruments, and temperature controllers.\n\nThe *azcam* package is currently used for Astronomical Research Cameras, Inc. Gen3, Gen2, and Gen1 CCD controllers, Magellan Guider controllers, STA Archon controllers, and CMOS cameras using ASCOM. Hadrware-specific code is found in azcam *extension* packages. \n\nSee *azcam-tool* for a common extension package which implements a GUI used by many observers.\n\n## Documentation\n\nSee https://mplesser.github.io/azcam/\n\nSee https://github.com/mplesser/azcam-tool.git for the standard GUI used by most telescope observers.\n\n## Installation\n\n`pip install azcam`\n\nOr download the latest version from from github: https://github.com/mplesser/azcam.git.\n\nYou may need to install `python3-tk` on Linux systems [`sudo apt-get install python3-tk`].\n\n## Startup and configuration\n\nAn *azcamserver* process is really only useful with a customized configuration script and environment which defines the hardware to be controlled.  Configuration scripts from existing environments may be used as examples. They would be imported into a python or IPython session or uses a startup script such to create a new server or console application. \n',
    'author': 'Michael Lesser',
    'author_email': 'mlesser@arizona.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mplesser/azcam/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
