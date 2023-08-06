# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bingus', 'bingus.environ', 'bingus.file', 'bingus.logging']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bingus',
    'version': '0.3.0',
    'description': 'Many python utilities in one package.',
    'long_description': '# Bingus: the package\n\nBingus is a library of utility scripts and functions.\n\nDocumentation can be found [here](https://bingus.readthedocs.io).\n\n## Generate Documentation\n\nYou can generate the documentation running `make html` in the `docs` directory.\n\n1. `cd docs`\n2. `make html`\n\nThen open the documentation by opening `./docs/_build/html/index.html` in your browser of\nchoice ([ideally Firefox](https://itsfoss.com/why-firefox/)).',
    'author': 'Bruno Robert',
    'author_email': 'contact.bruno@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/brunorobert/bingus',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
