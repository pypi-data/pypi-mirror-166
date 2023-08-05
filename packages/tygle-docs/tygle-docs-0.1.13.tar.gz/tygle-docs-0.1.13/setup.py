# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tygle_docs',
 'tygle_docs.base',
 'tygle_docs.rest',
 'tygle_docs.types',
 'tygle_docs.types.enums',
 'tygle_docs.types.requests',
 'tygle_docs.types.requests.models',
 'tygle_docs.types.resources',
 'tygle_docs.types.resources.models',
 'tygle_docs.types.resources.named_ranges',
 'tygle_docs.types.resources.named_ranges.named_range',
 'tygle_docs.types.resources.named_ranges.named_range.range',
 'tygle_docs.types.resources.structural_element',
 'tygle_docs.types.resources.structural_element.paragraph',
 'tygle_docs.types.resources.structural_element.paragraph.paragraph_element',
 'tygle_docs.types.resources.structural_element.paragraph.paragraph_element.text_run',
 'tygle_docs.types.resources.structural_element.table',
 'tygle_docs.types.resources.structural_element.table.table_row',
 'tygle_docs.types.resources.structural_element.table.table_row.table_cell',
 'tygle_docs.types.resources.structural_element.table.table_row.table_cell.table_cell_style',
 'tygle_docs.types.responses',
 'tygle_docs.utils']

package_data = \
{'': ['*']}

install_requires = \
['tygle>=0.2,<0.3']

setup_kwargs = {
    'name': 'tygle-docs',
    'version': '0.1.13',
    'description': '',
    'long_description': '',
    'author': 'shmookoff',
    'author_email': 'shmookoff@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
