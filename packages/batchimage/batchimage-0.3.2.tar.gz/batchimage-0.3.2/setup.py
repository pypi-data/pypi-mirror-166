# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['batchimage']

package_data = \
{'': ['*']}

install_requires = \
['opencv-python>=4.5.0,<5.0.0', 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['dot2dict = batchimage.batch_image_cli.py:start']}

setup_kwargs = {
    'name': 'batchimage',
    'version': '0.3.2',
    'description': 'Batch Image Converter',
    'long_description': '# Batch Image Processing\n\n\nA Python Package for Fast Parallel Processing of Images. It\'s Simple, easy and extremely fast since it uses, all the cores in your CPU. batchimage uses opencv-python as its main dependency and few python core modules.\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/batchimage?style=for-the-badge)\n\n### Python Package Index Badges\n\n[![PyPI](https://img.shields.io/pypi/v/batchimage?style=for-the-badge&color=gree&logo=pypi)](https://pypi.org/project/batchimage/)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/batchimage?label=Downloads&style=for-the-badge)\n![PyPI - Status](https://img.shields.io/pypi/status/batchimage?label=Status&style=for-the-badge)\n![PyPI - Format](https://img.shields.io/pypi/format/batchimage?label=Format&style=for-the-badge)\n\n\n### Github Badges\n\n![GitHub last commit](https://img.shields.io/github/last-commit/insumanth/batchimage?style=for-the-badge)\n![GitHub commit activity](https://img.shields.io/github/commit-activity/y/insumanth/batchimage?style=for-the-badge)\n![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/insumanth/batchimage?style=for-the-badge)\n![Lines of code](https://img.shields.io/tokei/lines/github/insumanth/batchimage?style=for-the-badge)\n\n\n\n------------------\n## Python Package Index Install \n\n```\npip install batchimage\n```\n\n### Note :\nThis is a pre-alpha version of the package, the api will change without any notice. Please use this package with caution.\n\n<!--\nTable\n-->\n\n### Timeline for Development\n\n| Present |                              September 2022                               |                              October 2022                               | November\'22                                                                  |\n|:---:|:-------------------------------------------------------------------------:|:-----------------------------------------------------------------------:|------------------------------------------------------------------------------|\n| ![Pre-Alpha](https://img.shields.io/badge/0-PRE--ALPHA-red?style=for-the-badge) | ![Alpha](https://img.shields.io/badge/1-ALPHA-orange?style=for-the-badge) | ![Beta](https://img.shields.io/badge/2-BETA-yellow?style=for-the-badge) | ![Release](https://img.shields.io/badge/3-RELEASE-green?style=for-the-badge) |\n\n\n\n-----------------\n![Made With Python](https://forthebadge.com/images/badges/made-with-python.svg)\n![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)\n\n<!--\n<img src="https://forthebadge.com/images/badges/works-on-my-machine.svg" alt="works-on-my-machine" width="500" height="100">\n-->\n',
    'author': 'Sumanth',
    'author_email': 'sumanthreddystar@gmail.com',
    'maintainer': 'Sumanth',
    'maintainer_email': 'sumanthreddystar@gmail.com',
    'url': 'https://pypi.org/project/batchimage/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
