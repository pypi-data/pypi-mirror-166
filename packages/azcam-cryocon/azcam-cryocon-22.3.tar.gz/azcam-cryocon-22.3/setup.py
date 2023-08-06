# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azcam_cryocon']

package_data = \
{'': ['*']}

install_requires = \
['azcam']

setup_kwargs = {
    'name': 'azcam-cryocon',
    'version': '22.3',
    'description': 'Azcam extension for Cryo-con temperature controllers',
    'long_description': '# azcam-cryocon\n\n*azcam-cryocon* is an *azcam* extension for Cryogenic Control Systems Inc. (cryo-con) temperature controllers. See http://www.cryocon.com/.\n\n## Installation\n\n`pip install azcam-cryocon`\n\nOr download from github: https://github.com/mplesser/azcam-cryocon.git.\n\n## Example Code\n\nThe code below is for example only.\n\n### Temperature Controller\n\n```python\nimport azcam.server\nfrom azcam_cryocon.tempcon_cryocon24 import TempConCryoCon24\ntempcon = TempConCryoCon24()\ntempcon.description = "cryoconqb"\ntempcon.host = "10.0.0.44"\ntempcon.control_temperature = -100.0\ntempcon.init_commands = [\n"input A:units C",\n"input B:units C",\n"input C:units C",\n"input A:isenix 2",\n"input B:isenix 2",\n"input C:isenix 2",\n"loop 1:type pid",\n"loop 1:range mid",\n"loop 1:maxpwr 100",\n]\n```\n',
    'author': 'Michael Lesser',
    'author_email': 'mlesser@arizona.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mplesser/azcam-cryocon/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
