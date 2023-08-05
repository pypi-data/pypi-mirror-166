# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['instagram_sync',
 'instagram_sync.contrib',
 'instagram_sync.contrib.django',
 'instagram_sync.contrib.django.migrations',
 'instagram_sync.core',
 'instagram_sync.core.graph_api']

package_data = \
{'': ['*'], 'instagram_sync.contrib.django': ['templates/instagram_sync/*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

extras_require = \
{'django': ['Django>=3.0', 'django-encrypted-model-fields>=0.6.5,<0.7.0']}

setup_kwargs = {
    'name': 'instagram-sync',
    'version': '0.1.8',
    'description': '',
    'long_description': None,
    'author': 'MJ Hardin',
    'author_email': 'mhardinla@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
