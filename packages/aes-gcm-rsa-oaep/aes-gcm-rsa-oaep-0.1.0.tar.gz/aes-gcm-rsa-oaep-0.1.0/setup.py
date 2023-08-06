# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aes_gcm_rsa_oaep']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=37.0.4,<38.0.0']

setup_kwargs = {
    'name': 'aes-gcm-rsa-oaep',
    'version': '0.1.0',
    'description': 'Kubeseal aes-gcm-rsa-oaep encryption implemented in python',
    'long_description': None,
    'author': 'Sascha Desch',
    'author_email': 'sascha.desch@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
