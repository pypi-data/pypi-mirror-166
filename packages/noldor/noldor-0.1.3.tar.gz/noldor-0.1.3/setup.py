# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['noldor', 'noldor.validators']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'noldor',
    'version': '0.1.3',
    'description': 'A validation library easy to extend.',
    'long_description': '# Noldor\n\nNoldor is a validation library easy to extend.',
    'author': 'Nicolò Sala',
    'author_email': 'nicolo.sala@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
