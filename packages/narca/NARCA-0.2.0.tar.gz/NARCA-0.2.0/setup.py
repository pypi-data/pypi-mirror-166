# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['narca']

package_data = \
{'': ['*']}

install_requires = \
['griddly>=1.4,<2.0',
 'hyperstate>=0.4.1,<0.5.0',
 'icecream>=2.1,<3.0',
 'matplotlib>=3.2,<4.0',
 'neptune-client>=0.16,<0.17',
 'numpy>=1.17,<2.0',
 'pyglet>=1.3,<2.0',
 'tensorboard>=2.9,<3.0',
 'tensorboardX>=2.5,<3.0']

setup_kwargs = {
    'name': 'narca',
    'version': '0.2.0',
    'description': 'NARS Controlled Agent: an agent capable of playing various games in Gym environments, using NARS for planning.',
    'long_description': 'None',
    'author': 'Adrian Borucki',
    'author_email': 'ab@synthillect.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
