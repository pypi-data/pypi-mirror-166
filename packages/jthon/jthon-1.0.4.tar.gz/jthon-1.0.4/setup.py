# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jthon']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jthon',
    'version': '1.0.4',
    'description': 'A JSON helper for Python',
    'long_description': '\n=======\n Jthon\n=======\nThis is a utility to make working with JSON files easier.\n\nInstallation \n=============\n\npip install jthon\n\nUsage\n------\n\n.. code-block:: python\n\n    import jthon\n    a_new_dict = {\n        \'fruits\': {\n            \'pineapple\':0,\n            \'apples\': 2,\n            \'orange\': 4,\n            \'pears\': 1\n        }\n    }\n    example = jthon.load(\'fruits\', a_new_dict)\n    find = example.find(key=\'apple\', exact=False)\n    for found in find:\n        print("I\'ve found \'{}\', with a value of \'{}\'.".format(found.key, found.value))\n        print("{}".format(found.siblings))\n\n    print("There are {} oranges in the dict!".format(example.get(\'fruits\').get(\'orange\')))\n    example[\'fruits\'][\'peach\'] = 1\n    example.save()\n    print(example)\n\nMore examples can be found in the examples folder\n\nRequirements\n-------------\n\n.. code:: python\n    \n    python3.5 >\n\n\n\n\nAuthors\n=======\n* **StroupBSlayen** - [GitHub](https://github.com/stroupbslayen)\n* **ProbsJustin** - [GitHub](https://github.com/SobieskiCodes)\n\nLicense\n========\n\nThis project is licensed under MIT - see the [LICENSE](LICENSE.txt) file for details',
    'author': 'StroupBSlayen',
    'author_email': '29642143+stroupbslayen@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stroupbslayen/jthon',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
