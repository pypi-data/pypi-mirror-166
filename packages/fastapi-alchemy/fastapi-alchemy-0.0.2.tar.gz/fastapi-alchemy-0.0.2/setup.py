# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_alchemy']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy[asyncio]>=1.4.40,<2.0.0',
 'aiomysql==0.1.1',
 'greenlet==1.1.3',
 'pytest==6.2.5']

setup_kwargs = {
    'name': 'fastapi-alchemy',
    'version': '0.0.2',
    'description': '',
    'long_description': None,
    'author': 'teamhide',
    'author_email': 'padocon@naver.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
