# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['osint_tools',
 'osint_tools.api',
 'osint_tools.api.four_chan',
 'osint_tools.db',
 'osint_tools.db.mongo_db',
 'osint_tools.schemas']

package_data = \
{'': ['*']}

install_requires = \
['feedparser>=6.0.10,<7.0.0',
 'motor>=3.0.0,<4.0.0',
 'pydantic>=1.10.1,<2.0.0',
 'python-jose>=3.3.0,<4.0.0',
 'requests>=2.11']

setup_kwargs = {
    'name': 'osint-tools',
    'version': '0.1.4',
    'description': '',
    'long_description': "# Python library for parsing various API's\n\n\n\n",
    'author': 'Alexander Slessor',
    'author_email': 'alexjslessor@gmail.com.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
