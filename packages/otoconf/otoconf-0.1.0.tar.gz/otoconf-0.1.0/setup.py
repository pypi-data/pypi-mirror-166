# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['otoconf']

package_data = \
{'': ['*']}

install_requires = \
['nginxfmt>=0.1.0', 'typer>=0.3.0']

setup_kwargs = {
    'name': 'otoconf',
    'version': '0.1.0',
    'description': 'oto generate configuration for proxy tools.',
    'long_description': '# oto generate configuration for proxy tools\n',
    'author': 'Bilal Alpaslan',
    'author_email': 'm.bilal.alpaslan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BilalAlpaslan/otoconf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
