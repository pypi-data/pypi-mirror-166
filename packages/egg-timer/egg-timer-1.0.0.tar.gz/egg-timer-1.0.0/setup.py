# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['egg_timer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'egg-timer',
    'version': '1.0.0',
    'description': 'A simpler way to handle timeouts in Python',
    'long_description': None,
    'author': 'Mike Salvatore',
    'author_email': 'mike.s.salvatore@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
