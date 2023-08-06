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
    'version': '0.3.0',
    'description': 'A simple client for Redis',
    'long_description': '# Redis client\n\nSimple Redis client for python.\n\nIt has been made to simplify working with Redis in python.\n\n## Usage\nInstantiate `Cache()`, give the Redis `host`, `port` and `db`.\n\nThen you can get a cached entry with `Cache.get_data_from_cache()` and add an entry to Redis with `Cache.save_data_to_cache()`\n\n**⚠️The data send to cache NEEDS TO BE A DICTIONARY! ⚠️**\n\n### Code example\n\n```python\nfrom redis_client.client import Cache\nfrom time import sleep\nfrom tpying import Dict\n\ncache = Cache(redis_host="localhost", redis_port=6379, redis_db=0, log_level="INFO")\n\ndef username_expander(username: str) -> Dict[str, str]:\n    """Example of a function that require caching."""\n    # Key that will be use to retrieve cached data\n    # Note that I include the parameter \'username\' in the key to make sure we only cache unique value.\n    key = f"username_expander:{username}"\n    # Check if the data is already caches\n    cached_data = cache.get_data_from_cache(key)\n    # Return it if yes\n    if cached_data:\n        return cached_data\n    \n    sleep(10)\n    data = {"expanded_username": f"{username}_123"}\n    # Save data to cache with an expiration time of 12 hours\n    cache.save_data_to_cache(key, data, expiration_in_hours=12)\n    return data\n```',
    'author': 'GraphtyLove',
    'author_email': 'maxim.berge@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/GraphtyLove/redis_client_python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
