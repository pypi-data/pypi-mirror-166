# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['formy', 'formy.tests']

package_data = \
{'': ['*'], 'formy': ['templates/formy/fields/*', 'templates/formy/form/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0', 'valley>=1.5.8,<2.0.0']

setup_kwargs = {
    'name': 'formy',
    'version': '1.3.1',
    'description': 'Valley is a Python forms library that allows you to use Jinja2 templates to create and manage the HTML of your forms.',
    'long_description': 'None',
    'author': 'Brian Jinwright',
    'author_email': 'bjinwright@qwigo.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
