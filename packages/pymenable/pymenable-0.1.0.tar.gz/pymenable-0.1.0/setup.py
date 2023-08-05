# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pymenable', 'pymenable.builders', 'pymenable.elements']

package_data = \
{'': ['*'], 'pymenable': ['templates/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0']

setup_kwargs = {
    'name': 'pymenable',
    'version': '0.1.0',
    'description': 'Python classes to render accessible HTML elements ',
    'long_description': '# pymenable\n\nPython classes to render accessible HTML elements \n\n## Installation\n\n```bash\n$ pip install pymenable\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`pymenable` was created by Joel Dodson. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`pymenable` was created with\n[`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/)\nand the\n[`py-pkgs-cookiecutter` template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n\nThe initial code for `pymenable` and the `examples`, came from the `ui` and `uiTest` (respectively) packages from the\n[`aclu` (Accessible Command Line Utilities) project](https://github.com/ringcentral/aclu)\nI started while at RingCentral.\n\nThe structure of the code including boilerplate for documentation and packaging came from the\n[book on Python Packaging, _Python Packages_](https://py-pkgs.org/).\n',
    'author': 'Joel Dodson',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
