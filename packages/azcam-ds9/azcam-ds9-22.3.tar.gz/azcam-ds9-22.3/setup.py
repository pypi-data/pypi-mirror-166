# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azcam_ds9']

package_data = \
{'': ['*']}

install_requires = \
['astropy', 'azcam', 'numpy']

setup_kwargs = {
    'name': 'azcam-ds9',
    'version': '22.3',
    'description': "Azcam extension for SAO's ds9 image display",
    'long_description': '# azcam-ds9\n\n## Purpose\n\n*azcam-ds9* is an *azcam extension* which supports SAO\'s ds9 display tool running under Windows. See https://sites.google.com/cfa.harvard.edu/saoimageds9.\n\nSee https://github.com/mplesser/azcam-ds9-winsupport for support code which may be helpful when displaying images on Windows computers\n\n## Display Class\nThis class defines Azcam\'s image display interface to SAO\'s ds9 image display. \nIt is usually instantiated as the *display* object for both server and clients.\n\nDepending on system configuration, the *display* object may be available \ndirectly from the command line, e.g. `display.display("test.fits")`.\n\nUsage Example:\n\n```python\nfrom azcam_ds9.ds9display import Ds9Display\ndisplay = Ds9Display()\ndisplay.display("test.fits")\nrois = display.get_rois(0, "detector")\nprint(rois)\n```\n\n## Installation\n\n`pip install azcam-ds9`\n\nOr download from github: https://github.com/mplesser/azcam-ds9.git.\n\n## Code Documentation\n\nhttps://mplesser.github.io/azcam-ds9\n\n## Notes\n\nIt may be helpful to remove all associations of .fits files in the registry and then only\nexecute the above batch files.  Do not directly associate .fits files with ds9.exe.',
    'author': 'Michael Lesser',
    'author_email': 'mlesser@arizona.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mplesser/azcam-ds9/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
