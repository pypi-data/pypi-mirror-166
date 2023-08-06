# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fido2-dev', 'fido2-dev.attestation', 'fido2-dev.ctap2', 'fido2-dev.hid']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=2.6,!=35,<40']

extras_require = \
{'pcsc': ['pyscard>=1.9,<3']}

setup_kwargs = {
    'name': 'fido2-dev',
    'version': '1.0.1.dev0',
    'description': 'FIDO2/WebAuthn library for implementing clients and servers.',
    'long_description': 'None',
    'author': 'Dain Nilsson',
    'author_email': 'dain@yubico.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Yubico/python-fido2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
