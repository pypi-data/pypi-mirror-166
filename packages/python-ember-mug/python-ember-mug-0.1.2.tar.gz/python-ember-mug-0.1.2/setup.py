# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ember_mug', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['bleak>=0.15.1,<0.16.0']

setup_kwargs = {
    'name': 'python-ember-mug',
    'version': '0.1.2',
    'description': 'Python Library for Ember Mugs.',
    'long_description': "# Python Ember Mug\n\n[![pypi](https://img.shields.io/pypi/v/python-ember-mug.svg)](https://pypi.org/project/python-ember-mug/)\n[![python](https://img.shields.io/pypi/pyversions/python-ember-mug.svg)](https://pypi.org/project/python-ember-mug/)\n[![Build Status](https://github.com/sopelj/python-ember-mug/actions/workflows/dev.yml/badge.svg)](https://github.com/sopelj/python-ember-mug/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/sopelj/python-ember-mug/branch/main/graphs/badge.svg)](https://codecov.io/github/sopelj/python-ember-mug)\n\nPython Library for Ember Mugs\n\n* Documentation: <https://sopelj.github.io/python-ember-mug>\n* GitHub: <https://github.com/sopelj/python-ember-mug>\n* PyPI: <https://pypi.org/project/python-ember-mug/>\n* Free software: MIT\n\n## Summary\n\nLibrary to attempt to interact with Ember Mugs via Bluetooth using the bleak library.\nThis was created for use with my [Home Assistant integration](https://github.com/sopelj/hass-ember-mug-component),\nbut could be useful separately and has a simple CLI interface too.\n\n**Note**: I have only tested with my Ember Mug 2, but others should work. (Please let me know)\n\n## Features\n\n* Finding mugs\n* Connecting to Mugs\n* Reading Information (Colour, temp, liquid level, etc.)\n* Polling for changes\n\n## Usage\n\n### CLI\nPut your mug in pairing mode (hold button five seconds or until blue)\n\n```bash\npython -m ember_mug discover  # Finds the mug in pairing mode for the first time\npython -m ember_mug poll  # fetches info and keeps listening for notifications\n```\n\n### Python\n\n```python\nfrom ember_mug.scanner import find_mug, discover_mugs\nfrom ember_mug.mug import EmberMug\n\n# if first time with mug in pairing\nmugs = await discover_mugs()\ndevice = mugs[0]\n# after paired you can simply use\ndevice = await find_mug()\nmug = EmberMug(device)\nasync with mug.connection() as con:\n    print('Connected.\\nFetching Info')\n    await con.update_all()\n    print(mug.formatted_data)\n```\n\n## Caveats\n\n- Since this api is not public, a lot of guesswork and reverse engineering is involved, so it's not perfect.\n- Only works with one mug at a time\n- These mugs do not broadcast data unless paired. So you can only have one device connected to it. You need to reset them to change to another device and make sure the previous device doesn't try to reconnect.\n- Reading data from the mug seems to work pretty well, but I have been unable to write to it so far... I always get NotPermitted errors.\n- I haven't figured out some attributes like udsk, dsk, location,\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.\n",
    'author': 'Jesse Sopel',
    'author_email': 'jesse.sopel@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sopelj/python-ember-mug',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
