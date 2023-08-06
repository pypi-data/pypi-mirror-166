# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pango_collapse']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.4,<2.0.0',
 'pango-aliasor>=0.2.0,<0.3.0',
 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['pango-collapse = pango_collapse.main:app']}

setup_kwargs = {
    'name': 'pango-collapse',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Pango-collapse \n\nCLI to collapse Pango linages for reporting\n\n## Install \n\nInstall from pypi with pip.\n\n```\npip install pango-collapse\n```\n\n',
    'author': 'wytamma',
    'author_email': 'wytamma.wirth@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
