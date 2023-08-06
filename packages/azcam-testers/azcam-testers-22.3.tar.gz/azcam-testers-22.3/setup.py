# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azcam_testers']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2', 'azcam', 'markdown', 'numpy', 'pdfkit', 'scipy']

setup_kwargs = {
    'name': 'azcam-testers',
    'version': '22.3',
    'description': 'Azcam extension for sensor characterization',
    'long_description': '# azcam-testers\n\n*azcam-testers* is an *azcam* extension used for image sensor characterization. It provides acquisition and analysis programs to characterize sensor performace such as:\n\n - quantum efficiency\n - gain and read noise\n - charge transfer efficiency\n - photon transfer\n - dark signal\n - photo-response non-uniformity\n - extended pixel edge response\n - bias frame analysis\n - defect analysis\n - response calibration\n - linearity\n - metrology\n - superflats\n\n## Documentation\n\nSee https://mplesser.github.io/azcam-testers/\n\n## Installation\n\n`pip install azcam-testers`\n\nOr download from github: https://github.com/mplesser/azcam-testers.git.\n\n## Usage Example\n\n```python\nqe.acquire()  # acquire QE image sequence \nqe.analyze()  # analyze the QE image sequence\n```\n',
    'author': 'Michael Lesser',
    'author_email': 'mlesser@arizona.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mplesser/azcam-testers/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
