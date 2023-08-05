# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['th2_cli', 'th2_cli.install_versions', 'th2_cli.utils', 'th2_cli.utils.helm']

package_data = \
{'': ['*']}

install_requires = \
['avionix>=0.4.5,<0.5.0',
 'cassandra-driver>=3.25.0,<4.0.0',
 'colorama>=0.4.5,<0.5.0',
 'cryptography>=37.0.4,<38.0.0',
 'fire>=0.4.0,<0.5.0',
 'kubernetes>=24.2.0,<25.0.0',
 'simple-term-menu>=1.5.0,<2.0.0']

entry_points = \
{'console_scripts': ['th2 = th2_cli:cli']}

setup_kwargs = {
    'name': 'th2-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Run\n\n```\npoetry install\npoetry shell\n```\n\n```commandline\nth2 install\n```',
    'author': 'Nikolay Dorofeev',
    'author_email': 'dorich2000@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
