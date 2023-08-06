# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_factory_pattern']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'simple-factory-pattern',
    'version': '1.3.1',
    'description': 'Simple way to prevent direct creation of an instance of a class.',
    'long_description': "# Simple Python Factory pattern\n\n![PyPI package](https://github.com/mammo0/py-simple-factory-pattern/workflows/PyPI%20package/badge.svg)\n[![PyPI version](https://badge.fury.io/py/simple-factory-pattern.svg)](https://badge.fury.io/py/simple-factory-pattern)\n\nThis module provides a simple way to prevent the direct creation of an instance of a class. Instead a `classmethod` of this class can be used.\n\n\n### Install\n\nYou can install this python module via **pip**:\n```shell\npip install simple-factory-pattern\n```\n\nOtherwise the module can be downloaded from PyPI: https://pypi.org/project/simple-factory-pattern/\n\n\n### Usage\n\n1. Import the module:\n   ```python\n   from simple_factory_pattern import FactoryPatternMeta\n   ```\n2. Create a class that uses the above meta class:\n   ```python\n   class NewClass(metaclass=FactoryPatternMeta):\n       pass\n   ```\n3. Add a `classmethod` to the new class that returns an instance of the class:\n   ```python\n   @classmethod\n   def create_instance(cls):\n       return NewClass()\n   ```\n   You can choose any name for the method. But it must be a `classmethod`!\n\n   It's also possible to define multiple `classmethod`s. Only in those methods a new instance of the class can be created.\n\n\n### Behavior of the new class\n\nIt's not possible to create an instance of the class directly:\n```python\ninstance = NewClass()  # this will fail\n```\nThis throws a `FactoryException` (also included in the `simple_factory_pattern` package).\n\nThe only way to get an instance is to call the above definded `classmethod`:\n```python\ninstance = NewClass.create_instance()  # this works\n```\n",
    'author': 'Marc Ammon',
    'author_email': 'marc.ammon@hotmail.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mammo0/py-simple-factory-pattern',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
