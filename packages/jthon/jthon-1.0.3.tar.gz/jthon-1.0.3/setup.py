# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jthon']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jthon',
    'version': '1.0.3',
    'description': 'Some stuff to make JSON easier to work with',
    'long_description': None,
    'author': 'StroupBSlayen',
    'author_email': '29642143+stroupbslayen@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
