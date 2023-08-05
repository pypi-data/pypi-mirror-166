# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['libdata', 'libdata.models']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'SQLAlchemy-Utils>=0.38.3,<0.39.0',
 'SQLAlchemy>=1.4.39,<2.0.0',
 'alembic>=1.8.1,<2.0.0',
 'artifacts-keyring>=0.3.2,<0.4.0',
 'asyncpg>=0.26.0,<0.27.0',
 'click>=8.1.3,<9.0.0',
 'coverage>=6.4.2,<7.0.0',
 'fastapi>=0.79.0,<0.80.0',
 'ipython>=8.4.0,<9.0.0',
 'jsql>=0.8,<0.9',
 'keyring>=23.8.2,<24.0.0',
 'mangum>=0.15.1,<0.16.0',
 'psycopg2-binary>=2.9.3,<3.0.0',
 'pydantic[email]>=1.9.2,<2.0.0',
 'pylint>=2.15.0,<3.0.0',
 'pytest-azurepipelines>=1.0.3,<2.0.0',
 'pytest-bdd>=6.0.1,<7.0.0',
 'pytest-cov>=3.0.0,<4.0.0',
 'pytest-mock>=3.8.2,<4.0.0',
 'pytest>=7.1.2,<8.0.0',
 'requests>=2.28.1,<3.0.0',
 'setuptools>=65.3.0,<66.0.0',
 'uvicorn>=0.18.2,<0.19.0']

setup_kwargs = {
    'name': 'df-data-lib',
    'version': '0.0.6',
    'description': '',
    'long_description': None,
    'author': 'sufyanaligit',
    'author_email': 'informsufyan@gmail.com',
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
