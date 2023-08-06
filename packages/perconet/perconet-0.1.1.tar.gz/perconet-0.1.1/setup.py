# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['perconet']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.3,<2.0.0']

setup_kwargs = {
    'name': 'perconet',
    'version': '0.1.1',
    'description': 'Analyze percolation properties of periodic networks',
    'long_description': '========\nperconet\n========\n\nOverview\n========\n\nThe **perconet** package provides tools to analyze the percolation properties of\nperiodic nets or networks. The terminology to describe such systems varies between\nfields (see the sections *for mathematicians* and *for chemists* in the documentation).\n\nPeriodic networks arise often in simulations of chemical or physical systems with\n*periodic boundary conditions*. Since periodic nets have no actual boundaries, the\nquestion whether they percolate must be interpreted as *does the structure wrap around\nthe periodic boundary*?\n\n**perconet** implements a loop finder algorithm that reports the number of *independent*\nways in which the structure wraps around the boundary.\n\nDocumentation\n=============\n*Will add links to docs after setting up readthedocs account*\n\nRelease Status\n==============\nThis is a development release that has been extensively tested in a few contexts but\nwe cannot guarantee it will work as you will expect. If you get unexpected results\nand suspect you found a bug, please open an issue on github.\n\n\nCredits and License\n===================\nPerconet was written by Chiara Raffaelli and Wouter G. Ellenbroek.\nIssue reports and contributions are welcome through our `GitHub repository <https://github.com/wouterel/perconet>`_\n\nWe share **perconet** under the European Union Public License. See LICENSE file for details.',
    'author': 'Chiara Raffaelli, Wouter G. Ellenbroek',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/wouterel/perconet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
