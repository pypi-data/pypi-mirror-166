# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['choicetypes']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'choicetypes',
    'version': '0.1.0rc0',
    'description': 'Powerful and simple algebraic sum types in Python.',
    'long_description': '# Python Choice Types\n\n`choicetypes` brings powerful and simple algebraic [sum types](https://en.wikipedia.org/wiki/Tagged_union) to Python.\n\n## Usage\n\nNew `Choice` types are constructed using sytax similar to standard library enums and dataclasses:\n\n```python\nfrom choicetypes import Choice\n\n\nclass IpAddr(Choice):\n    V4: tuple[int, int, int, int]\n    V6: str\n\n\nhome = IpAddr(V4=(127, 0, 0, 1))\nloopback = IpAddr(V6="::1")\n```\n\nA choice consists of mutually exclusive _variants_. In this example, any instance of `IpAddr` must be **either** a `V4` or `V6` address. Variants are just normal attributes and can be accessed as such. But they\'re also designed to work seamlessly with [structural pattern matching](https://peps.python.org/pep-0636/), introduced in Python 3.10:\n\n```python\nfor ip in (home, loopback):\n    match ip:\n        case IpAddr(V4=fields):\n            print("{}:{}:{}:{}".format(*fields))\n        case IpAddr(V6=text):\n            print(text)\n```\n\nFor a complete overview of what `Choice` type can do, see the [official documentation](https://samwaterbury.github.io/choicetypes/).\n\n## Installation\n\nThe `choicetypes` package is available on PyPi:\n\n```shell\npip install choicetypes\n```\n\nIt is written in pure Python and has zero dependencies.\n\n## Background\n\nAlgebraic choice types have various other names (sum types, tagged unions, etc.) and exist in a number of programming languages. The primary inspiration for `choicetypes` was Rust\'s [Enum type](https://doc.rust-lang.org/book/ch06-00-enums.html).\n\nPython\'s `Enum` allows you to express mutually exclusive variants, but not associated data. Its `dataclass` (and similar) types store data but cannot represent mutually exclusive variants. The core idea behind algebraic sum types is to store these two pieces of information simultaneously.\n\nI wanted to build a type that could accomplish this in a similar style to Rust. Importantly, it had to work cleanly with structural pattern matching and type hinting.\n',
    'author': 'Sam Waterbury',
    'author_email': 'samwaterbury1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/samwaterbury/choicetypes',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
