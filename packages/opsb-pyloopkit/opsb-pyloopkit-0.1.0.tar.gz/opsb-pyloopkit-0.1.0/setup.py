# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyloopkit', 'pyloopkit.depreciated']

package_data = \
{'': ['*'],
 'pyloopkit': ['docs/*', 'example_files/*', 'tests/fixtures/LoopKit/*']}

install_requires = \
['numpy>=1.23.2,<2.0.0']

setup_kwargs = {
    'name': 'opsb-pyloopkit',
    'version': '0.1.0',
    'description': '',
    'long_description': "# PyLoopKit\nA set of Python tools for building closed-loop insulin delivery apps (Python port of LoopKit)\n\n[Link to Tidepool Loop repository version used for algorithm](https://github.com/tidepool-org/Loop/tree/8c1dfdba38fbf6588b07cee995a8b28fcf80ef69)\n\n[Link of Tidepool LoopKit repository version used for algorithm](https://github.com/tidepool-org/LoopKit/tree/57a9f2ba65ae3765ef7baafe66b883e654e08391)\n\n# To use this project\n## Please review [the documentation](pyloopkit/docs/pyloopkit_documentation.md) for usage instructions, input data requirements, and other important details.\n\n### To recreate the Virtual Environment\n1. This environment was developed with Anaconda. You'll need to install [Miniconda](https://conda.io/miniconda.html) or [Anaconda](https://anaconda-installer.readthedocs.io/en/latest/) for your platform.\n2. In a terminal, navigate to the directory where the environment.yml \nis located (likely in PyLoopKit/pyloopkit folder).\n3. Run `conda env create`; this will download all of the package dependencies\nand install them in a virtual environment named py-loop. PLEASE NOTE: this\nmay take up to 30 minutes to complete.\n\n### To use the Virtual Environment\nIn Bash run `source activate py-loop`, or in the Anaconda Prompt\nrun `conda activate py-loop` to start the environment.\n\nRun `deactivate` to stop the environment.\n\n### To create the PyLoopKit package\nIf you want to install a version of the PyLoopKit package based on the PyLoopKit on your local machine, run `python3 setup.py install` within your PyLoopKit repo to call the setup script and install the package. You'll likely want to do this within the `py-loop` environment.\n\n### Running the unittests\nTo run PyLoopKit's unit tests, run `python3 -m unittest discover` within your PyLoopKit repo\n",
    'author': 'Oliver Searle-Barnes',
    'author_email': 'oliver@opsb.co.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tidepool-org/PyLoopKit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
