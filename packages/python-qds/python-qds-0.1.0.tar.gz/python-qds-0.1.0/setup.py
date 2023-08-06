# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qds']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-qds',
    'version': '0.1.0',
    'description': 'A Python wrapper for Quartz Display Services.',
    'long_description': '# QDS\n\nA Python wrapper for [Quartz Display Services](https://developer.apple.com/documentation/coregraphics/quartz_display_services).\n',
    'author': 'Kamil Turek',
    'author_email': 'kamil.turek@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kamilturek/qds',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<3.12',
}


setup(**setup_kwargs)
