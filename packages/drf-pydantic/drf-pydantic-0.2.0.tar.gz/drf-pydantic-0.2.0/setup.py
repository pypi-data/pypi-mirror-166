# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['drf_pydantic']

package_data = \
{'': ['*']}

install_requires = \
['djangorestframework>=3.13.0,<4.0.0', 'pydantic[email]>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'drf-pydantic',
    'version': '0.2.0',
    'description': 'Use pydantic with the Django REST framework',
    'long_description': '<p align="center">\n  <a href="https://github.com/georgebv/drf-pydantic/actions/workflows/cicd.yml" target="_blank">\n    <img src="https://github.com/georgebv/drf-pydantic/actions/workflows/cicd.yml/badge.svg?branch=main" alt="CI/CD Status">\n  </a>\n  <a href="https://codecov.io/gh/georgebv/drf-pydantic" target="_blank">\n    <img src="https://codecov.io/gh/georgebv/drf-pydantic/branch/main/graph/badge.svg?token=GN9rxzIFMc" alt="Test Coverage"/>\n  </a>\n  <a href="https://badge.fury.io/py/drf-pydantic" target="_blank">\n    <img src="https://badge.fury.io/py/drf-pydantic.svg" alt="PyPI version" height="18">\n  </a>\n</p>\n\n<p align="center">\n  <i>\n    Use pydantic with Django REST framework\n  </i>\n</p>\n\n- [Introduction](#introduction)\n- [Installation](#installation)\n- [Usage](#usage)\n  - [General](#general)\n  - [Custom Base Models](#custom-base-models)\n- [Roadmap](#roadmap)\n\n# Introduction\n\n[Pydantic](https://pydantic-docs.helpmanual.io) is a great Python library to perform\ndata serialization and validation.\n\n[Django REST framework](https://www.django-rest-framework.org) is a framework built\non top of [Django](https://www.djangoproject.com/) which allows writing REST APIs.\n\nIf like me you develop DRF APIs and you like pydantic , `drf-pydantic` is for you 😍.\n\n# Installation\n\n```shell\npip install drf-pydantic\n```\n\n# Usage\n\n## General\n\nUse `drf_pydantic.BaseModel` instead of `pydantic.BaseModel` when creating your\nmodels:\n\n```python\nfrom drf_pydantic import BaseModel\n\nclass MyModel(BaseModel):\n  name: str\n  addresses: list[str]\n```\n\nWhenever you need a DRF serializer you can get it from the model like this:\n\n```python\nMyModel.drf_serializer\n```\n\n> ℹ️ **INFO**<br>\n> Models created using `drf_pydantic` are fully idenditcal to those created by\n> `pydantic` and only the `drf_serializer` attribute is added on class creation.\n\n## Custom Base Models\n\nYou can also use it as a mixin with your existing pydantic models (no need to change\nyour existing code 🥳):\n\n```python\nfrom drf_pydantic import BaseModel as DRFBaseModel\nfrom pydantic import BaseModel\n\nclass MyBaseModel(BaseModel):\n  value: int\n\nclass MyModel(DRFBaseModel, MyBaseModel):\n  name: str\n  addresses: list[str]\n```\n\n> ⚠️ **ATTENTION**<br>\n> Inheritance order is important: `drf_pydantic.BaseModel` must always go before\n> the `pydantic.BaseModel` class.\n\n# Roadmap\n\n- Add `ENUM` support\n- Add option to create custom serializer for complex models\n',
    'author': 'George Bocharov',
    'author_email': 'bocharovgeorgii@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/georgebv/drf-pydantic',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
