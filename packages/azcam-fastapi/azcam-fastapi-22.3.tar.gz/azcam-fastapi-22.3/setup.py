# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azcam_fastapi']

package_data = \
{'': ['*']}

install_requires = \
['azcam', 'fastapi', 'jinja2', 'uvicorn']

setup_kwargs = {
    'name': 'azcam-fastapi',
    'version': '22.3',
    'description': 'Azcam-fastapi is an azcam extension which implements a fastapi-based webserver',
    'long_description': '# azcam-fastapi\n\n*azcam-fastapi* is an *azcam* extension which adds support for a fastapi-based web server.\n\n## Installation\n\n`pip install azcam-fastapi`\n\nor download from github: https://github.com/mplesser/azcam-fastapi.git.\n\n## Uage Example\n\n```python\nfrom azcam_fastapi.fastapi_server import WebServer\nwebserver = WebServer()\nwebserver.index = f"index_mysystem.html"\nwebserver.start()\n```\n',
    'author': 'Michael Lesser',
    'author_email': 'mlesser@arizona.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mplesser/azcam-fastapi/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
