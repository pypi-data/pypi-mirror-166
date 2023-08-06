# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bobifi']

package_data = \
{'': ['*'], 'bobifi': ['data/*']}

setup_kwargs = {
    'name': 'bobifi',
    'version': '2022.9.6',
    'description': 'BoB Metadata Keys and URLs',
    'long_description': '# BoB Metadata Keys and URLs\n\nThis repository contains a Python module with the current [BoB](https://bob.samtrafiken.se/) Metadata keys and URLs. Inspired by [certifi](https://github.com/certifi/python-certifi).\n\n\n## Installation\n\n`bobifi` is available on PyPI. Simply install it with ``pip``:\n\n    $ pip install bobifi\n\n\n## Usage\n\n`bobify` includes test and production keys and metadata URLs from Swedish Samtrafiken. Usage examples below.\n\n    >>> from bobifi.samtrafiken import trusted_jwks, metadata_url, where\n\n    >>> metadata_url(env="test")\n    \'https://bobmetadata-pp.samtrafiken.se/api/v2/participantMetadata\'\n\n    >>> where(env="test")\n    \'/home/bob/bobifi/data/samtrafiken-test.json\'\n\n    >>> import pprint\n    >>> pprint.pprint(trusted_jwks(env="test"))\n    {\'keys\': [{\'crv\': \'P-256\',\n               \'kid\': \'16:samtrafiken_one\',\n               \'kty\': \'EC\',\n               \'x\': \'f83OJ3D2xF1Bg8vub9tLe1gHMzV76e8Tus9uPHvRVEU\',\n               \'y\': \'x_FEzRu9m36HLN_tue659LNpXW6pCyStikYjKIWI5a0\'},\n              {\'e\': \'AQAB\',\n               \'kid\': \'16:samtrafiken_fallback_2023\',\n               \'kty\': \'RSA\',\n               \'n\': \'t5ITeoklTnhR8XNDLYKx5WsUxkJZkBSqT-5dfc-W_1cByD0ZKf-2DkwArXWwK4bYPQ2RlDuot-m8U2GSjnQ9wNxrA1oIUzJZYw1ryqbq-Lh1hrbYWbW2OlcIIce2dzEnSdbphTthoYFDu1xS8n5hi1xC-LGlmfmQfTCjCZR5CFnRbar97rAjfrRfvlwG15XJTC6BiDtYZMF5KmpgKCqP39ELCqV0LHXfeJ50v263a9enlD0RogNAbwM0OTDZ-ek8WF5YePEuE1p0-Pbe14O-pSkT_DPwl5pF6uk6QN3whr90oTgDkUoI4xb88jhscWb1yf4PfjsF3F4JUgYn9V1w28-N7ZIkGe6-PznWmvjsgJj9u6sg9f2-AU5k2ZsZCuO1-bVSubjJU0j2J7DyvP3wpxt1ybrOjA1X8K2s6bMBan0u3CsHDsikGHsgKlDkWJvD5fBpb1Ize3YfbAJvbGNtT2ae6Ft0cB__xVGDvJqEl6UHZgU4gBm01DiX20RJcGgWbX5nsz47mC2zXG_thtpPd8lAsyevGBKTsMpPEomAwRfL_VDWvjcXGPTD7Lm-igzzWLHrK9xRmhBOHs_oxK2o6gUtu4LcqSh1PHCIzBznzdacHVSPrLy5pPTuwxm4DYrhycOvlb8PPL9qX7qscJTwp5jcNYAYvmF2Ezns32HhIXM\'}]}\n\n\nFor Samtrafiken, the `test` and `prod` environments are currently defined. The `prod` environment is used as default.\n\n',
    'author': 'Jakob Schlyter',
    'author_email': 'jakob@kirei.se',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': "https://github.com/kirei/python-bobifi'",
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
