# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['micro_metrics', 'micro_metrics.bp', 'micro_metrics.dmo', 'micro_metrics.svc']

package_data = \
{'': ['*']}

install_requires = \
['baseblock']

setup_kwargs = {
    'name': 'micro-metrics',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Craig Trim',
    'author_email': 'craigtrim@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.5',
}


setup(**setup_kwargs)
