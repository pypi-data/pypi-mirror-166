# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['satchel']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pysatchel',
    'version': '0.0.0a1',
    'description': 'Satchel is a compendium of pure python functions to carry with you and get things done.',
    'long_description': '# Satchel\n\nSatchel is a compendium of pure python functions to carry with you and get things done.\n\n## Installation\n\n```\npip install PySatchel\n```\n\n## Usage\n\n```python\n>>> import satchel.iterable import chunk\n\n>>> some_list = [1, 2, 3, 4, 5]\n>>> chunk(some_list, 2, "length", True)\n# [[1, 2], [3, 4], [5]]\n\n>>> chunk(some_list, 2, "count", True)\n# [[1, 2, 3], [3, 5]]\n```\n',
    'author': 'Taylor Beever',
    'author_email': 'taybeever@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/theelderbeever/satchel',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
