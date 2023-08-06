# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aislib']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3,<4.0',
 'numpy>=1.2,<2.0',
 'pandas-plink>=2.2.4,<3.0.0',
 'pandas>=1.2,<2.0',
 'py>=1.10.0,<2.0.0',
 'scikit-learn>=1,<2',
 'seaborn>=0,<1',
 'sympy>=1,<2',
 'torch>=1,<2',
 'torchvision>=0,<1',
 'tqdm>=4.55,<5.0']

setup_kwargs = {
    'name': 'aislib',
    'version': '0.1.8a0',
    'description': '',
    'long_description': None,
    'author': 'Arnor Sigurdsson',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
