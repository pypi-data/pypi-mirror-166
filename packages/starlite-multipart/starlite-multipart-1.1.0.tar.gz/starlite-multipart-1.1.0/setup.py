# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starlite_multipart']

package_data = \
{'': ['*']}

install_requires = \
['anyio']

setup_kwargs = {
    'name': 'starlite-multipart',
    'version': '1.1.0',
    'description': 'Toolkit for working with multipart/formdata messages.',
    'long_description': 'None',
    'author': "Na'aman Hirschfeld",
    'author_email': 'nhirschfeld@gmail.com',
    'maintainer': "Na'aman Hirschfeld",
    'maintainer_email': 'nhirschfeld@gmail.com',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
