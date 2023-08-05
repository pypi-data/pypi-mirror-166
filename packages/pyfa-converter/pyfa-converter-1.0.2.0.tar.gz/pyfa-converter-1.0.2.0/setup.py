# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfa_converter', 'pyfa_converter.utils']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.65', 'pydantic>=1.6', 'python-multipart>=0.0.5,<0.0.6']

setup_kwargs = {
    'name': 'pyfa-converter',
    'version': '1.0.2.0',
    'description': 'Pydantic to fastapi model converter.',
    'long_description': 'None',
    'author': 'dotX12',
    'author_email': 'dev@shitposting.team',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dotX12/pyfa-converter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
