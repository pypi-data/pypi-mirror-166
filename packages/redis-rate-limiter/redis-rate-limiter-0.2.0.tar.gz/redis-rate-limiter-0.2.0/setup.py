# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redis_rate_limiter']

package_data = \
{'': ['*']}

install_requires = \
['redis>=1']

setup_kwargs = {
    'name': 'redis-rate-limiter',
    'version': '0.2.0',
    'description': 'A Redis based rate limiter implementation for Python',
    'long_description': "# redis-rate-limiter\n\n[![CI](https://github.com/duyixian1234/redis-rate-limiter/actions/workflows/CI.yml/badge.svg?branch=master)](https://github.com/duyixian1234/redis-rate-limiter/actions/workflows/CI.yml)\n\n## Install\n\n```bash\npip install -U redis-rate-limiter\n```\n\n## Use\n\n```python\nfrom redis_rate_limiter.config import basic_config\nfrom redis_rate_limiter.rate_limiter import RateLimiter\n\nbasic_config(redis_url='redis://localhost:6379/0')\n\n@RateLimiter(10, period=1)\ndef greet():\n    print('Hello')\n\nfor _ in range(100):\n    greet()\n\n# Raise RateLimitExceeded after print('Hello') 10 times\n```\n",
    'author': 'duyixian',
    'author_email': 'duyixian1234@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/duyixian1234/redis-rate-limiter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
