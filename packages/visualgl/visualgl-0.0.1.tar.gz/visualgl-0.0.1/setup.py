# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['visualgl', 'visualgl.filetypes.stl', 'visualgl.messaging', 'visualgl.opengl']

package_data = \
{'': ['*']}

install_requires = \
['PyOpenGL>=3.1.6,<4.0.0',
 'glfw>=2.5.4,<3.0.0',
 'numpy>=1.23.1,<2.0.0',
 'spatial3d>=0.7.0,<0.8.0']

extras_require = \
{'extras': ['PyOpenGL-accelerate>=3.1.6,<4.0.0']}

setup_kwargs = {
    'name': 'visualgl',
    'version': '0.0.1',
    'description': 'A Python library for visualizations with OpenGL.',
    'long_description': '# visualgl v0.0.1 ![Badge](https://github.com/jbschwartz/visualgl/actions/workflows/ci.yml/badge.svg)\nA Python library for visualizations with OpenGL.\n\n**Note: This library is currently being factored out from the [robotpy](https://github.com/jbschwartz/robotpy) application and is still very experimental.**\n\n## Installation\n\nInstall using `pip`:\n\n```\npython -m pip install visualgl\n```\n\nInstall using `poetry`:\n\n```\npoetry add visualgl\n```\n',
    'author': 'James Schwartz',
    'author_email': 'james@schwartz.engineer',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jbschwartz/visualgl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
