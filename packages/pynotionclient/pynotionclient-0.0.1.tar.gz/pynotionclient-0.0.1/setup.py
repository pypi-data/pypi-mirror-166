# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pynotionclient']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=0.8.1,<0.9.0',
 'pydantic>=1.10.1,<2.0.0',
 'pylint-quotes>=0.2.3,<0.3.0',
 'pylint>=2.15.0,<3.0.0',
 'pytest-cov>=3.0.0,<4.0.0',
 'pytest>=7.1.3,<8.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'requests>=2.28.1,<3.0.0',
 'setuptools>=65.3.0,<66.0.0']

setup_kwargs = {
    'name': 'pynotionclient',
    'version': '0.0.1',
    'description': 'Python wrapper for Notion API',
    'long_description': None,
    'author': 'Vetrichelvan',
    'author_email': 'pythonhub.py@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
