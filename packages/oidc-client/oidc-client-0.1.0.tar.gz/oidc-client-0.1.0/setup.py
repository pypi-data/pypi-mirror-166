# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oidc_client']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.11"': ['toml>=0.10.2,<0.11.0']}

entry_points = \
{'console_scripts': ['oidc = oidc_client.cli:main']}

setup_kwargs = {
    'name': 'oidc-client',
    'version': '0.1.0',
    'description': 'A pure-Python OpenID Connect client',
    'long_description': 'OIDC Client\n===========\n\nA pure-Python OpenID Connect client supporting OAuth 2.1 authorization flows, built for Python 3.10+ with minimal dependencies.\n\nOAuth 2.1 authorization flows include:\n- the **authorization code** flow, for interactive user login;\n- the **client credentials** flow, for confidential machine-to-machine communication.\n\nThis OIDC Client supports reading configuration profiles from a `pyproject.toml` file.\n\n\nRequirements\n------------\n\nPython 3.10+\n\n\n\nInstallation\n------------\n\n```console\npip install oidc-client\n```\n\n\nExamples\n--------\n\n```console\n# To log-in as user, using a web browser:\noidc login --interactive\n```\n\n',
    'author': 'Loris Zinsou',
    'author_email': 'lzinsou@proton.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/lzinsou/oidc-client',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
