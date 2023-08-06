# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['matchy', 'matchy.matching_algorithms']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'numpy>=1.23.2,<2.0.0']

entry_points = \
{'console_scripts': ['matchy = matchy.cli:cli']}

setup_kwargs = {
    'name': 'matchy',
    'version': '0.1.1',
    'description': 'A tool for matching analog IC layout designs.',
    'long_description': "# matchy\n\nA tool for matching devices in analog layout in a streamlined and automated way.\n\n## Installation\n\nRun `pip install matchy` for the latest stable version.\n\n### Development\n\n1. Git clone [this repository](https://github.com/ftorres16/matchy/).\n2. `cd` to the root folder where this repo is cloned.\n3. `poetry install` to install it with [Python Poetry](https://python-poetry.org/).\n\n## Usage\n\n1. Write `matchy` in a terminal.\n2. The CLI will ask you for the number of devices you want to match.\n3. The CLI will ask you for the multiplicity of each device.\n4. Sit back and wait for the optimization to occur.\n5. You will be prompted with the system's best guess for the optimal matrix, as well as some key metrics, such as the centroid of each device and total error.\n\nYou may want to use `matchy` only to calculate the centroid of your devices. In that case:\n\n1. Save your device matrix configuration in a CSV file.\n2. Run `matchy --initial <PATH> --method do_nothing`\n3. Matchy will print the centroid for each device in a table.\n",
    'author': 'Fabian Torres',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ftorres16/matchy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
