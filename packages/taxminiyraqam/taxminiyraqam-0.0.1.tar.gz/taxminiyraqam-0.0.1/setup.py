# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['taxminiyraqam']
setup_kwargs = {
    'name': 'taxminiyraqam',
    'version': '0.0.1',
    'description': '',
    'long_description': '```python\nfrom taxminiyraqam import taxmin\nprint(taxmin(50))\n```',
    'author': 'Ozodbek Yusupov',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
