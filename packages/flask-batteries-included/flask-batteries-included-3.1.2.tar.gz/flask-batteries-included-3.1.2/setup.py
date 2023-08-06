# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_batteries_included',
 'flask_batteries_included.blueprint_debug',
 'flask_batteries_included.blueprint_monitoring',
 'flask_batteries_included.helpers',
 'flask_batteries_included.helpers.security']

package_data = \
{'': ['*']}

install_requires = \
['Flask-Log-Request-Id<1.0.0',
 'Flask>=2.0.0,<3.0.0',
 'apispec>=5.0.0,<6.0.0',
 'dhos-redis>=1.0.0,<2.0.0',
 'environs>=9.0.0,<10.0.0',
 'healthcheck>=1.0.0,<2.0.0',
 'marshmallow>=3.0.0,<4.0.0',
 'prometheus-client<1.0.0',
 'python-jose>=3.0.0,<4.0.0',
 'requests>=2.0.0,<3.0.0',
 'she-logging>=1.0.0,<2.0.0',
 'waitress>=2.0.0,<3.0.0']

extras_require = \
{'apispec': ['apispec-webframeworks<1.0.0',
             'connexion[swagger-ui]>=2.0.0,<3.0.0'],
 'pgsql': ['Flask-Migrate>=3.0.0,<4.0.0',
           'Flask-SQLAlchemy>=2.0.0,<3.0.0',
           'psycopg2-binary>=2.0.0,<3.0.0']}

setup_kwargs = {
    'name': 'flask-batteries-included',
    'version': '3.1.2',
    'description': 'Batteries-included library for Polaris microservices using Flask',
    'long_description': None,
    'author': 'Rob Grant',
    'author_email': 'rob.grant@sensynehealth.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/polaris-foundation/flask-batteries-included',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
