# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kombu_batteries_included']

package_data = \
{'': ['*']}

install_requires = \
['environs>=9.0.0,<10.0.0', 'kombu>=5.0.0,<6.0.0', 'she-logging>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'kombu-batteries-included',
    'version': '1.1.4',
    'description': 'Batteries-included library for Polaris services using Kombu',
    'long_description': None,
    'author': 'Jon Daly',
    'author_email': 'jonathan.daly@sensynehealth.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/polaris-foundation/kombu-batteries-included',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
