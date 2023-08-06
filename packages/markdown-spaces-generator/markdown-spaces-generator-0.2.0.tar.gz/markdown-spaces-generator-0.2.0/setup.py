# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['markdown_spaces_generator']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['markdown-spaces-generator = '
                     'markdown_spaces_generator.cli:main']}

setup_kwargs = {
    'name': 'markdown-spaces-generator',
    'version': '0.2.0',
    'description': '',
    'long_description': 'None',
    'author': '0djentd',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
