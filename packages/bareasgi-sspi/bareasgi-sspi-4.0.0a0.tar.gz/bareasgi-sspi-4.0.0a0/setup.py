# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bareasgi_sspi']

package_data = \
{'': ['*']}

install_requires = \
['bareutils>=4.0.1,<5.0.0',
 'jetblack-asgi-typing>=0.4.0,<0.5.0',
 'pyspnego>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'bareasgi-sspi',
    'version': '4.0.0a0',
    'description': 'ASGI middleware for SSPI',
    'long_description': '# bareASGI-sspi\n\nASGI middleware for SSPI authentication.\n\n## Installation\n\nInstall from the pie store.\n\n```\npip install bareasgi-sspi\n```\n\n',
    'author': 'Rob Blackbourn',
    'author_email': 'rob.blackbourn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rob-blackbourn/bareASGI-SSPI',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
