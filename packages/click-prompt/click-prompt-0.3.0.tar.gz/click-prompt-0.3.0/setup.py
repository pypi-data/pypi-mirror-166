# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['click_prompt']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.4', 'questionary>=1.10.0,<2.0.0']

setup_kwargs = {
    'name': 'click-prompt',
    'version': '0.3.0',
    'description': 'click-prompt provides more beautiful interactive options for the Python click library',
    'long_description': "# click-prompt\n\n[![Supported Python Versions](https://img.shields.io/pypi/pyversions/click-prompt)](https://pypi.org/project/click-prompt/) \n[![PyPI version](https://img.shields.io/pypi/v/click-prompt)](https://pypi.org/project/click-prompt/) \n\n\nclick-prompt provides more beautiful interactive options for the Python click\nlibrary. The library is inspired by a post on [stackoverflow.com](https://stackoverflow.com/questions/54311067/)\n\n## Usage\n\n```python\n\n\nimport click\nfrom click_prompt import ChoiceOption\n\n@click.command()\n@click.option('--fruit', \n              type=click.Choice(['Apples', 'Bananas', 'Grapefruits', 'Mangoes']),\n              cls=ChoiceOption)\ndef select_fruit(fruit: str):\n    print(choice)\n```\n\n\n## Available Parameters\n\nfor every click.Option there is also a click.Argument  implementation\n\n - ChoiceOption: Select a single item out of a list\n - MultipleOption: Select multiple items out of a list\n - ConfirmOption: Yes/No confirmation\n - FilePathOption: Select a file path with auto completion\n - AutoCompleteOption: Auto completion given a list\n\n",
    'author': 'Markus Grotz',
    'author_email': 'grotz@uw.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.9,<4.0',
}


setup(**setup_kwargs)
