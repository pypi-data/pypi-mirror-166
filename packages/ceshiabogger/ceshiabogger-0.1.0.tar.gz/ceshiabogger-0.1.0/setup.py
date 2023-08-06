# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ceshiabogger']

package_data = \
{'': ['*']}

install_requires = \
['PyMySQL>=1.0.2,<2.0.0', 'fastapi-utils>=0.2.1,<0.3.0']

setup_kwargs = {
    'name': 'ceshiabogger',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'laowang',
    'author_email': '847063657@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
