# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lava', 'lava.objects', 'lava.objects.filters']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.0,<4.0.0',
 'discord-py>=2.0.0,<3.0.0',
 'spoti-py>=0.1.0,<0.2.0',
 'typing_extensions>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'discord-ext-lava',
    'version': '0.5.0',
    'description': 'A discord.py extension for lavaplayer-based audio nodes.',
    'long_description': '# discord-ext-lava\nA [discord.py](https://github.com/Rapptz/discord.py) extension for [lavaplayer](https://github.com/Walkyst/lavaplayer-fork)-based audio nodes.\n\n## Support\n- [Documentation](https://discord-ext-lava.readthedocs.io/)\n- [GitHub](https://github.com/Axelware/discord-ext-lava)\n- [Discord](https://discord.com/invite/w9f6NkQbde)\n',
    'author': 'Axel',
    'author_email': 'axelancerr@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Axelware/discord-ext-lava',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.0,<4.0.0',
}


setup(**setup_kwargs)
