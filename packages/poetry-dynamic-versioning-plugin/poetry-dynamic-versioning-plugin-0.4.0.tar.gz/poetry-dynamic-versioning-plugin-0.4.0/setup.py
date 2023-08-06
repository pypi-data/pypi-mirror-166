# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_dynamic_versioning']

package_data = \
{'': ['*']}

install_requires = \
['dunamai>=1.12.0,<2.0.0',
 'jinja2>=2.11.1,<4',
 'poetry>=1.2.0,<2.0.0',
 'tomlkit>=0.4']

entry_points = \
{'poetry.application.plugin': ['poetry-dynamic-versioning-plugin = '
                               'poetry_dynamic_versioning.plugin:DynamicVersioningPlugin']}

setup_kwargs = {
    'name': 'poetry-dynamic-versioning-plugin',
    'version': '0.4.0',
    'description': 'Plugin for Poetry to enable dynamic versioning based on VCS tags',
    'long_description': '# Dynamic versioning plugin for Poetry\nThis is a Python 3.7+ plugin for [Poetry 1.2.0+](https://github.com/sdispater/poetry)\nto enable dynamic versioning based on tags in your version control system,\npowered by [Dunamai](https://github.com/mtkennerly/dunamai).\n\nThe package `poetry-dynamic-versioning-plugin` has been merged into\n[`poetry-dynamic-versioning`](https://pypi.org/project/poetry-dynamic-versioning),\nunder the optional feature named `plugin`. Please install that package instead.\n',
    'author': 'Matthew T. Kennerly',
    'author_email': 'mtkennerly@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mtkennerly/poetry-dynamic-versioning',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
