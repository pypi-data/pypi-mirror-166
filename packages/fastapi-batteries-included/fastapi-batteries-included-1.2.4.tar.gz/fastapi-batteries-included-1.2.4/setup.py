# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_batteries_included',
 'fastapi_batteries_included.helpers',
 'fastapi_batteries_included.helpers.security',
 'fastapi_batteries_included.router_monitoring']

package_data = \
{'': ['*']}

install_requires = \
['aiofile>=3.0.0,<4.0.0',
 'cachetools>=4.2.2,<5.0.0',
 'fastapi<1.0.0',
 'prometheus-client<1.0.0',
 'prometheus-fastapi-instrumentator>=5.0.0,<6.0.0',
 'she-logging>=1.0.0,<2.0.0',
 'typer<1.0.0']

extras_require = \
{'jwt': ['python-jose>=3.0.0,<4.0.0'],
 'mssql': ['SQLAlchemy[mypy]>=1.4.0,<1.5.0',
           'FastAPI-SQLAlchemy<1.0.0',
           'alembic>=1.0.0,<2.0.0',
           'pyodbc>=4.0.0,<5.0.0'],
 'pgsql': ['psycopg2-binary>=2.0.0,<3.0.0',
           'SQLAlchemy[mypy]>=1.4.0,<1.5.0',
           'FastAPI-SQLAlchemy<1.0.0',
           'alembic>=1.0.0,<2.0.0']}

entry_points = \
{'console_scripts': ['create-openapi = '
                     'fastapi_batteries_included.helpers.apispec:create_openapi']}

setup_kwargs = {
    'name': 'fastapi-batteries-included',
    'version': '1.2.4',
    'description': 'Batteries-included library for services that use FastAPI',
    'long_description': None,
    'author': 'Duncan Booth',
    'author_email': 'duncan.booth@sensynehealth.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/polaris-foundation/fastapi-batteries-included',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
