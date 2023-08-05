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
    'version': '0.1.1',
    'description': 'Python Gfycat API',
    'long_description': '# gpycat\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gpycat?style=for-the-badge)\n![GitHub](https://img.shields.io/github/license/kvdomingo/pygfycat?style=for-the-badge)\n![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/kvdomingo/pygfycat?include_prereleases&style=for-the-badge)\n\nThis is a WIP unofficial Python wrapper for the Gfycat web API.\n\n## Installation\n```shell\n# pip\npip install vlive\n\n# poetry\npoetry add vlive\n```\n\n## Usage\n\n```python\nfrom gpycat import gpycat\n\ngpycat.auth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)\nitem = gpycat.get_gfycat("zestycreepyasiaticlesserfreshwaterclam")\n```\n\nOutput:\n```shell\n> GfyItem(title="...", description="...", avgColor="...", content_urls={...}, ...)\n```',
    'author': 'Kenneth V. Domingo',
    'author_email': 'hello@kvdomingo.xyz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kvdomingo/pygfycat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
