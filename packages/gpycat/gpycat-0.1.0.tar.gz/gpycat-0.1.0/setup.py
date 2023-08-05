# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gpycat', 'gpycat.models']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0',
 'pydantic>=1.9.2,<2.0.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'gpycat',
    'version': '0.1.0',
    'description': 'Python Gfycat API',
    'long_description': '# gpycat\n\nPython Gfycat API (WIP)',
    'author': 'Kenneth V. Domingo',
    'author_email': 'hello@kvdomingo.xyz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kvdomingo/pygfycat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
