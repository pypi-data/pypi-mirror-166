# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kanagawa']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'kanagawa',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'benthecoder',
    'author_email': 'benthecoder07@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
