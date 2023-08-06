# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_singleton']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'simple-singleton',
    'version': '1.5.1',
    'description': 'Simple way to create a singleton class.',
    'long_description': '# Simple Python Singleton pattern\n\n![PyPI package](https://github.com/mammo0/py-simple-singleton/workflows/PyPI%20package/badge.svg)\n[![PyPI version](https://badge.fury.io/py/simple-singleton.svg)](https://badge.fury.io/py/simple-singleton)\n\nThis module provides a simple way to define a class as a singleton.\n\n\n### Install\n\nYou can install this python module via **pip**:\n```shell\npip install simple-singleton\n```\n\nOtherwise the module can be downloaded from PyPI: https://pypi.org/project/simple-singleton/\n\n\n### Usage\n\n1. Import the module:\n   ```python\n   from simple_signleton import Singleton\n   ```\n   or:\n   ```python\n   from simple_signleton import SingletonArgs\n   ```\n2. Create a class that uses one of the above meta classes:\n   ```python\n   class NewClass(metaclass=Singleton):\n       pass\n   ```\n   or:\n   ```python\n   class NewClass(metaclass=SingletonArgs):\n       pass\n   ```\n\n\n### Difference between `Singleton` and `SingletonArgs`\n\nThe `Singleton` class is a very basic implementation of the singleton pattern. All instances of a class are equal. Even if they are initialized with different parameters:\n```python\ninstance1 = SingletonClass(param="value")\ninstance2 = SingletonClass(param="different_value")\n\nassert instance1 == instance2  # True\nprint(instance2.param)         # "value"\n```\n\n**If you do not want this behavior**, use the `SingletonArgs` meta class. With this class only instances that are initialized with the same parameters are the equal:\n```python\ninstance1 = SingletonArgsClass(param="value")\ninstance2 = SingletonArgsClass(param="different_value")\ninstance3 = SingletonArgsClass(param="value")\n\nassert instance1 == instance2  # False\nassert instance1 == instance3  # True\n\nprint(instance2.param)         # "different_value"\n```\n\n\n### Usage in multi-threaded environments\n\n**The `Singleton` and `SingletonArgs` meta classes are not thread-safe!**\n\nTo use them in a multi-threaded environment, please use the\n\n- `ThreadSingleton` and\n- `ThreadSingletonArgs`\n\nmeta classes. They can be used exactly like the standard meta classes.\n',
    'author': 'Marc Ammon',
    'author_email': 'marc.ammon@hotmail.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mammo0/py-simple-singleton',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
