# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['py_mono_tools', 'py_mono_tools.backends', 'py_mono_tools.goals']

package_data = \
{'': ['*'], 'py_mono_tools': ['templates/*', 'templates/dockerfiles/*']}

install_requires = \
['Jinja2>=3,<4',
 'bandit>=1,<2',
 'black>=22,<23',
 'click>=8,<9',
 'flake8>=5,<6',
 'isort>=5,<6',
 'mypy>=0.971,<0.972',
 'pydocstringformatter>=0.7,<0.8',
 'pydocstyle[toml]>=6,<7',
 'pylint>=2,<3']

entry_points = \
{'console_scripts': ['pmt = py_mono_tools.main:cli',
                     'py_mono_tools = py_mono_tools.main:cli']}

setup_kwargs = {
    'name': 'py-mono-tools',
    'version': '0.0.4',
    'description': 'A CLI designed to make it easier to work in a python mono repo',
    'long_description': '# Python Mono Tools\n\n## Instillation\n\n`pip install py-mono-tools`\n\n## Usage\n\n`pmt lint`\n\n# More information\n\nFor more information, please go the GitHub page. https://peterhoburg.github.io/py_mono_tools/\n',
    'author': 'Peter Hoburg',
    'author_email': 'peterHoburg@users.noreply.github.com',
    'maintainer': 'Peter Hoburg',
    'maintainer_email': 'peterHoburg@users.noreply.github.com',
    'url': 'https://github.com/peterHoburg/py_mono_tools',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
