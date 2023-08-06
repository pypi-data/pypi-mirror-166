# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redis_client']

package_data = \
{'': ['*']}

install_requires = \
['redis==4.3.4']

setup_kwargs = {
    'name': 'redis-client',
    'version': '0.1.0',
    'description': 'A simple client for Redis',
    'long_description': '# Redis client',
    'author': 'GraphtyLove',
    'author_email': 'maxim.berge@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
