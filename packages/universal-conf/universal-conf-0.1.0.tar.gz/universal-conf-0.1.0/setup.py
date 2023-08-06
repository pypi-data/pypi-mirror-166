# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['universal_conf']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'universal-conf',
    'version': '0.1.0',
    'description': 'A universal configuration framework for Python projects.',
    'long_description': 'A universal configuration framework for Python projects.',
    'author': 'Isaac Beverly',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
