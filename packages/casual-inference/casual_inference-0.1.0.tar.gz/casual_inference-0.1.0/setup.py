# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['casual_inference', 'casual_inference.dataset']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.2,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'plotly>=5.10.0,<6.0.0',
 'scipy>=1.9.1,<2.0.0']

setup_kwargs = {
    'name': 'casual-inference',
    'version': '0.1.0',
    'description': '',
    'long_description': '# casual_inference\n\n[![ci](https://github.com/shyaginuma/casual_inference/actions/workflows/config.yml/badge.svg)](https://github.com/shyaginuma/casual_inference/actions/workflows/config.yml)\n\nDo A/B test analysis more easily.\n\n## Awesome resources related to Experimenation\n\nTBA\n',
    'author': 'yaginuuun',
    'author_email': 'yaginuuun@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shyaginuma',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
