# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wagtail_honeypot',
 'wagtail_honeypot.migrations',
 'wagtail_honeypot.templatetags',
 'wagtail_honeypot.test',
 'wagtail_honeypot.test.migrations',
 'wagtail_honeypot.test.tests']

package_data = \
{'': ['*'],
 'wagtail_honeypot': ['static/*',
                      'templates/*',
                      'templates/tags/*',
                      'templates/wagtail_honeypot_test/*'],
 'wagtail_honeypot.test': ['fixtures/*']}

install_requires = \
['Django>=3.0', 'wagtail>=2.14']

setup_kwargs = {
    'name': 'wagtail-honeypot',
    'version': '1.0.0',
    'description': 'Use this package to add optional honeypot protection to your Wagtail forms.',
    'long_description': None,
    'author': 'Nick Moreton',
    'author_email': 'nickmoreton@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
