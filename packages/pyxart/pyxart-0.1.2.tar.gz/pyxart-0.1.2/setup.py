# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyxart',
 'pyxart.client',
 'pyxart.exceptions',
 'pyxart.group',
 'pyxart.keys',
 'pyxart.server']

package_data = \
{'': ['*']}

install_requires = \
['XEdDSA>=0.6,<0.7',
 'cryptography>=37.0.4,<38.0.0',
 'matplotlib>=3.0,<4.0',
 'networkx>=2.5,<3.0',
 'pynacl>=1.5,<2.0']

setup_kwargs = {
    'name': 'pyxart',
    'version': '0.1.2',
    'description': 'Python implementation of Asynchronous Ratchet Trees',
    'long_description': '# pyxart\nPython implementation of Asynchronous Ratchet Trees\n\n# references\n\n- https://research.facebook.com/publications/on-ends-to-ends-encryption-asynchronous-group-messaging-with-strong-security-guarantees/',
    'author': 'Pranay Anchuri',
    'author_email': 'pranay@xmtp.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
