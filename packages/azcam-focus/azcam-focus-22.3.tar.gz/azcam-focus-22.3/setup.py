# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azcam_focus']

package_data = \
{'': ['*']}

install_requires = \
['azcam']

setup_kwargs = {
    'name': 'azcam-focus',
    'version': '22.3',
    'description': 'Azcam extension to control focus observations used to determine optimal instrument or telescope focus positions',
    'long_description': '# azcam-focus\n\n*azcam-focus* is an *azcam* extension to control focus observations used to determine optimal instrument or telescope focus position.\n\nThis code is usually executed in the console window although a server-side version is available on some systems.\n\n`focus` is an instance of the *Focus* class.\n\n## Code Documentation\n\nSee https://mplesser.github.io/azcam_focus/.\n\n## Installation\n\n`pip install azcam-focus`\n\nOr download from github: https://github.com/mplesser/azcam-focus.git.\n\n## Code Examples\n\n`focus.command(parameters...)`\n\n```python\nfocus.set_pars(1, 30, 10)  \nfocus.run()\n```\n\n## Parameters\n\nParameters may be changed from the command line as:\n`focus.number_exposures=7`\nor\n`focus.set_pars(1.0, 5, 25, 15)`.\n\n<dl>\n  <dt><strong>focus.number_exposures = 7</strong></dt>\n  <dd>Number of exposures in focus sequence</dd>\n\n  <dt><strong>focus.focus_step = 30</strong></dt>\n  <dd>Number of focus steps between each exposure in a frame</dd>\n\n  <dt><strong>focus.detector_shift = 10</strong></dt>\n  <dd>Number of rows to shift detector for each focus step</dd>\n\n  <dt><strong>focus.focus_position</strong></dt>\n  <dd>Current focus position</dd>\n\n  <dt><strong>focus.exposure_time = 1.0</strong></dt>\n  <dd>Exposure time (seconds)</dd>\n\n  <dt><strong>focus.focus_component = "instrument"</strong></dt>\n  <dd>Focus component for motion - "instrument" or "telescope"</dd>\n\n  <dt><strong>focus.focus_type = "absolute"</strong></dt>\n  <dd>Focus type, "absolute" or "step"</dd>\n\n  <dt><strong>focus.set_pars_called = 1</strong></dt>\n  <dd>Flag to not prompt for focus position</dd>\n\n  <dt><strong>focus.move_delay = 3</strong></dt>\n  <dd>Delay in seconds between focus moves</dd>\n</dl>\n',
    'author': 'Michael Lesser',
    'author_email': 'mlesser@arizona.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mplesser/azcam-focus/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
