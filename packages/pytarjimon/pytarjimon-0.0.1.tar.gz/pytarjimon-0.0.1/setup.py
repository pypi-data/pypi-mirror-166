# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pytarjimon']
install_requires = \
['googletrans==3.1.0a0']

setup_kwargs = {
    'name': 'pytarjimon',
    'version': '0.0.1',
    'description': '',
    'long_description': '```python\nfrom pytarjimon import tarjima\nnatija = tarjima("Hello", "uz")\nprint(natija)\n```',
    'author': 'Ozodbek Yusupov',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
