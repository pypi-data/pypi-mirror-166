# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['safely']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'safely',
    'version': '0.1.0',
    'description': 'Capture side effects, safely.',
    'long_description': '# safely\n',
    'author': 'Luke Miloszewski',
    'author_email': 'lukemiloszewski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lukemiloszewski/safely',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.0,<3.11.0',
}


setup(**setup_kwargs)
