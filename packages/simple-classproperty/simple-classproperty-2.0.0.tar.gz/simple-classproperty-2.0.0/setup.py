# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_classproperty']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'simple-classproperty',
    'version': '2.0.0',
    'description': "Provides a 'classproperty' decorator.",
    'long_description': '# Simple Python `classproperty` decorator\n\n![PyPI package](https://github.com/mammo0/py-simple-classproperty/workflows/PyPI%20package/badge.svg)\n[![PyPI version](https://badge.fury.io/py/simple-classproperty.svg)](https://badge.fury.io/py/simple-classproperty)\n\nThis module provides a simple way for defining class properties.\n\n\n----\n\n**Deprecation notice:** Starting with Python 3.9 the `@classmethod` descriptor can now wrap other descriptors like `@property`. See the official documentation for the announcement: https://docs.python.org/3.9/library/functions.html#classmethod\n\nThis means if you are using Python >= 3.9 you can simply realize a classproperty with:\n\n```python\nclass NewClass():\n    _atr = "val"\n\n    @classmethod\n    @property\n    def attr(cls):\n        return cls._atr\n```\n\nSo in this case this package is not needed anymore. I will still try to maintain this package until Python 3.8 reaches EOL which will be in October 2024.\n\n----\n\n\n### Install\n\nYou can install this Python module via **pip**:\n```shell\npip install simple-classproperty\n```\n\nOtherwise the module can be downloaded from PyPI: https://pypi.org/project/simple-classproperty/\n\n\n### Usage\n\n1. Import the module:\n   ```python\n   from simple_classproperty import ClasspropertyMeta, classproperty\n   ```\n2. Create a class with a class property:\n   ```python\n   class NewClass(metaclass=ClasspropertyMeta):\n       _attr = "val"\n\n       @classproperty\n       def attr(cls):\n           return cls._attr\n   ```\n   **Don\'t forget to set the `metaclass`!**\n3. **(Optional)** Define also a setter and deleter for the newly created class property (this works like the standard python `property`):\n   ```python\n   @attr.setter\n   def attr(cls, value):\n       cls._attr = value\n\n   @attr.deleter\n   def attr(cls):\n       del cls._attr\n   ```\n\n\n### Tips\n\nThe `classproperty` is also accessible from an instance:\n```python\ninstance = NewClass()\nprint(instance.attr)  # "val"\n```\n\nWhen the value of the property is changed from an instance object, the class property will be changed. All other instances will have this new value:\n```python\ninstance1 = NewClass()\ninstance2 = NewClass()\n\ninstance1.attr = "new"\n\nprint(instance1.attr)  # "new"\nprint(instance2.attr)  # "new"\nprint(NewClass.attr)   # "new"\n```\n\nThis behavior is the same when a property gets deleted from an instance.\n',
    'author': 'Marc Ammon',
    'author_email': 'marc.ammon@hotmail.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mammo0/py-simple-classproperty',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)
