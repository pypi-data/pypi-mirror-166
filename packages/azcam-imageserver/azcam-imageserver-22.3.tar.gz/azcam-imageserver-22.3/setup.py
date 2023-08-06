# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azcam_imageserver']

package_data = \
{'': ['*']}

install_requires = \
['azcam']

setup_kwargs = {
    'name': 'azcam-imageserver',
    'version': '22.3',
    'description': 'Azcam extension to suuport a remote image server',
    'long_description': '# azcam-imageserver\n\n*azcam-imageserver* is an *azcam* extension which supports sending an image to a remote host running an image server which receives the image.\n\n## Installation\n\n`pip install azcam-imageserver`\n\nOr download from github: https://github.com/mplesser/azcam-imageserver.git.\n\n## Usage\n\n```python\nfrom azcam_imageserver.sendimage import SendImage\nsendimage = SendImage()\nremote_imageserver_host = "10.0.0.1"\nremote_imageserver_port = 6543\nsendimage.set_remote_imageserver(remote_imageserver_host, remote_imageserver_port, "azcam")\n```\n',
    'author': 'Michael Lesser',
    'author_email': 'mlesser@arizona.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mplesser/azcam-imageserver/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
