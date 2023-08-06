# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['content_negotiation']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'content-negotiation',
    'version': '1.0.0',
    'description': 'A library for deciding content-type based on media ranges in HTTP Accept headers.',
    'long_description': '# content-negotiation\n\n![Tests](https://github.com/Informasjonsforvaltning/content-negotiation/workflows/Tests/badge.svg)\n[![codecov](https://codecov.io/gh/Informasjonsforvaltning/content-negotiation/branch/master/graph/badge.svg)](https://codecov.io/gh/Informasjonsforvaltning/content-negotiation)\n[![PyPI](https://img.shields.io/pypi/v/content-negotiation.svg)](https://pypi.org/project/content-negotiation/)\n[![Read the Docs](https://readthedocs.org/projects/content-negotiation/badge/)](https://content-negotiation.readthedocs.io/)\n\nA small Python library for deciding content type based on a list of media ranges\n\n## Usage\n\n### Install\n\n```Shell\n% pip install content-negotiation\n```\n\n### Getting started\n\n```Python\nfrom content_negotiation import decide_content_type\n\naccept_headers = ["application/json", "text/html", "text/plain, text/*;q=0.8"]\nsupported_content_types = ["text/turtle", "application/json"]\n\ntry:\n    content_type = decide_content_type(accept_headers, supported_content_types)\nexcept NoAgreeableContentTypeError:\n    print("No agreeable content type found.")\n    # Handle error, by returning e.g. 406 Not Acceptable\n```\n\n## Development\n\n### Requirements\n\n- [pyenv](https://github.com/pyenv/pyenv) (recommended)\n- python3\n- [pipx](https://github.com/pipxproject/pipx) (recommended)\n- [poetry](https://python-poetry.org/)\n- [nox](https://nox.thea.codes/en/stable/)\n\n```Shell\n% pipx install poetry==1.1.13\n% pipx install nox==2022.1.7\n% pipx inject nox nox-poetry==0.9.0\n```\n\n### Install developer tools\n\n```Shell\n% git clone https://github.com/Informasjonsforvaltning/content-negotiation.git\n% cd content-negotiation\n% pyenv install 3.8.12\n% pyenv install 3.9.10\n% pyenv local 3.8.12 3.9.10 \n% poetry install\n```\n\n### Run all sessions\n\n```Shell\n% nox\n```\n\n### Run all tests with coverage reporting\n\n```Shell\n% nox -rs tests\n```\n\n### Debugging\n\nYou can enter into [Pdb](https://docs.python.org/3/library/pdb.html) by passing `--pdb` to pytest:\n\n```Shell\n% nox -rs tests -- --pdb  --log-cli-level=DEBUG\n```\n\nYou can set breakpoints directly in code by using the function `breakpoint()`.\n',
    'author': 'Amund Tenstad',
    'author_email': 'github@amund.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Informasjonsforvaltning/content-negotiation',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
