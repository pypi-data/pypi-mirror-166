# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splinator', 'splinator.tests']

package_data = \
{'': ['*']}

install_requires = \
['cvxopt>=1.3.0,<2.0.0',
 'numpy>=1.19.0,<2.0.0',
 'pandas>=1.3.0,<2.0.0',
 'scikit-learn>=1.0.0,<2.0.0',
 'scipy>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'splinator',
    'version': '0.1.0',
    'description': 'Python library for fitting linear-spine based logistic regression for calibration.',
    'long_description': None,
    'author': 'Jiarui Xu',
    'author_email': 'jiarui.xu@affirm.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
