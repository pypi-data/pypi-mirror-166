# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['w6libs', 'w6libs.PyPDF2', 'w6libs.PyPDF2._codecs', 'w6libs.PyPDF2.generic']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'w6-libs',
    'version': '0.0.1',
    'description': 'W6 Library',
    'long_description': 'W6 Library Package.\n\nChange Log\n================\n0.0.1 (Sep 6, 2022)\n- First Release\n',
    'author': 'Irawan',
    'author_email': 'irawan@waresix.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/irawanahak/w6-libs',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
