# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cal9000', 'cal9000.render']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['cal9000 = cal9000.__main__:main']}

setup_kwargs = {
    'name': 'cal9000',
    'version': '0.1.0',
    'description': 'Vim enabled version of cal(1)',
    'long_description': "# cal9000\n\nVim enabled version of [cal(1)](https://linux.die.net/man/1/cal).\n\n## Why?\n\nI want to get better about using calendars, but I don't like the thought of\nusing an online one. I also wanted something that I could use from the CLI\nwith ease, and be very effecient with it.\n\n## Installing and Running\n\n```\n$ pip install cal9000\n$ cal9000\n```\n\n## Usage\n\nPress `?` to view help.\n\n## Configuration\n\nTBD\n\n## Testing\n\n```\n$ git clone https://github.com/dosisod/cal9000\n$ cd cal9000\n$ python3 -m virtualenv .venv\n$ source .venv/bin/activate\n$ pip3 install -r dev-requirements.txt\n```\n",
    'author': 'dosisod',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dosisod/cal9000',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
