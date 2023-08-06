# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['w6libs', 'w6libs.PyPDF2', 'w6libs.PyPDF2._codecs', 'w6libs.PyPDF2.generic']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'w6-libs',
    'version': '0.0.2',
    'description': 'W6 Library',
    'long_description': 'W6 Library Package.\n\nChange Log\n================\n0.0.1 (Sep 6, 2022)\n- First Release\n\n0.0.2 (Sep 9, 2022)\n- Fix dependency\n\n',
    'author': 'Irawan',
    'author_email': 'irawan@waresix.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/irawanahak/w6-libs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
