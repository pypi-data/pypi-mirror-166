# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['safe_url_analyzers',
 'safe_url_analyzers.analyzers',
 'safe_url_analyzers.models.analyzers']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-serialization>=1.3.1,<2.0.0',
 'google-cloud-webrisk>=1.6.1,<2.0.0',
 'pydantic>=1.7,<2.0']

setup_kwargs = {
    'name': 'safe-url-analyzers',
    'version': '0.4.0',
    'description': '',
    'long_description': None,
    'author': 'Tùng Đỗ Sơn',
    'author_email': 'svtt.tungds@vccloud.vn',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
