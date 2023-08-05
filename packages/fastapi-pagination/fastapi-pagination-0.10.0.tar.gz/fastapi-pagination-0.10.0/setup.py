# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_pagination', 'fastapi_pagination.ext', 'fastapi_pagination.links']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.80.0', 'pydantic>=1.9.1']

extras_require = \
{'all': ['SQLAlchemy>=1.3.20',
         'databases>=0.6.0',
         'orm>=0.3.1',
         'tortoise-orm>=0.16.18,<0.20.0',
         'asyncpg>=0.24.0',
         'ormar>=0.11.2',
         'Django<3.3.0',
         'piccolo>=0.89.0,<0.90.0',
         'motor>=2.5.1,<4.0.0',
         'mongoengine>=0.23.1,<0.25.0',
         'sqlmodel>=0.0.8,<0.0.9'],
 'asyncpg': ['SQLAlchemy>=1.3.20', 'asyncpg>=0.24.0'],
 'databases': ['databases>=0.6.0'],
 'django': ['databases>=0.6.0', 'Django<3.3.0'],
 'mongoengine': ['mongoengine>=0.23.1,<0.25.0'],
 'motor': ['motor>=2.5.1,<4.0.0'],
 'orm': ['databases>=0.6.0', 'orm>=0.3.1'],
 'ormar': ['ormar>=0.11.2'],
 'piccolo': ['piccolo>=0.89.0,<0.90.0'],
 'sqlalchemy': ['SQLAlchemy>=1.3.20'],
 'sqlmodel': ['sqlmodel>=0.0.8,<0.0.9'],
 'tortoise': ['tortoise-orm>=0.16.18,<0.20.0']}

setup_kwargs = {
    'name': 'fastapi-pagination',
    'version': '0.10.0',
    'description': 'FastAPI pagination',
    'long_description': '<h1 align="center">FastAPI Pagination</h1>\n\n<div align="center">\n<img alt="license" src="https://img.shields.io/badge/License-MIT-lightgrey">\n<img alt="test" src="https://github.com/uriyyo/fastapi-pagination/workflows/Test/badge.svg">\n<img alt="codecov" src="https://codecov.io/gh/uriyyo/fastapi-pagination/branch/main/graph/badge.svg?token=QqIqDQ7FZi">\n<a href="https://pepy.tech/project/fastapi-pagination"><img alt="downloads" src="https://pepy.tech/badge/fastapi-pagination"></a>\n<a href="https://pypi.org/project/fastapi-pagination"><img alt="pypi" src="https://img.shields.io/pypi/v/fastapi-pagination"></a>\n<img alt="black" src="https://img.shields.io/badge/code%20style-black-000000.svg">\n</div>\n\n## Introduction\n\n`fastapi-pagination` is a library that provides pagination feature for [FastAPI](https://fastapi.tiangolo.com/)\napplications.\n\n----\n\nFor more information about library please see [documentation](https://uriyyo-fastapi-pagination.netlify.app/).\n\n---\n\n## Installation\n\n```bash\npip install fastapi-pagination\n```\n\n## Quickstart\n\nAll you need to do is to use `Page` class as a return type for your endpoint and call `paginate` function\non data you want to paginate.\n\n```py\nfrom fastapi import FastAPI\nfrom pydantic import BaseModel, Field\n\nfrom fastapi_pagination import Page, add_pagination, paginate  # import all you need from fastapi-pagination\n\napp = FastAPI()  # create FastAPI app\n\n\nclass UserOut(BaseModel):  # define your model\n    name: str = Field(..., example="Steve")\n    surname: str = Field(..., example="Rogers")\n\n\nusers = [  # create some data\n    # ...\n]\n\n\n@app.get(\'/users\', response_model=Page[UserOut])  # use Page[UserOut] as response model\nasync def get_users():\n    return paginate(users)  # use paginate function to paginate your data\n\n\nadd_pagination(app)  # important! add pagination to your app\n```\n\nPlease, be careful when you work with databases, because default `paginate` will require to load all data in memory.\n\nFor instance, if you use `SQLAlchemy` you can use `paginate` from `fastapi_pagination.ext.sqlalchemy` module.\n\n```py\nfrom fastapi_pagination.ext.sqlalchemy import paginate\n\n\n@app.get(\'/users\', response_model=Page[UserOut])\ndef get_users(db: Session = Depends(get_db)):\n    return paginate(db.query(User).order_by(User.created_at))\n```\n\nFor `SQLAlchemy 2.0 style` you can use `paginate` from `fastapi_pagination.ext.sqlalchemy_future` module.\n\n```py\nfrom sqlalchemy import select\nfrom fastapi_pagination.ext.sqlalchemy_future import paginate\n\n\n@app.get(\'/users\', response_model=Page[UserOut])\ndef get_users(db: Session = Depends(get_db)):\n    return paginate(db, select(User).order_by(User.created_at))\n```\n\nCurrently, `fastapi-pagination` supports:\n\n| Library                                                                                     | `paginate` function                                 | \n|---------------------------------------------------------------------------------------------|-----------------------------------------------------|\n| [SQLAlchemy](https://docs.sqlalchemy.org/en/14/orm/quickstart.html)                         | `fastapi_pagination.ext.sqlalchemy.paginate`        |\n| [SQLAlchemy 2.0 style](https://docs.sqlalchemy.org/en/14/changelog/migration_20.html)       | `fastapi_pagination.ext.sqlalchemy_future.paginate` |\n| [Async SQLAlchemy 2.0 style](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html) | `fastapi_pagination.ext.async_sqlalchemy.paginate`  |\n| [SQLModel](https://sqlmodel.tiangolo.com/)                                                  | `fastapi_pagination.ext.sqlmodel.paginate`          |\n| [Async SQLModel](https://sqlmodel.tiangolo.com/)                                            | `fastapi_pagination.ext.async_sqlmodel.paginate`    |\n| [AsyncPG](https://magicstack.github.io/asyncpg/current/)                                    | `fastapi_pagination.ext.asyncpg.paginate`           |\n| [Databases](https://www.encode.io/databases/)                                               | `fastapi_pagination.ext.databases.paginate`         |\n| [Django ORM](https://docs.djangoproject.com/en/3.2/topics/db/queries/)                      | `fastapi_pagination.ext.django.paginate`            |\n| [GINO](https://python-gino.org/)                                                            | `fastapi_pagination.ext.gino.paginate`              |\n| [MongoEngine](https://docs.mongoengine.org/)                                                | `fastapi_pagination.ext.mongoengine.paginate`       |\n| [Motor](https://motor.readthedocs.io/en/stable/)                                            | `fastapi_pagination.ext.motor.paginate`             |\n| [ORM](https://www.encode.io/orm/)                                                           | `fastapi_pagination.ext.orm.paginate`               |\n| [ormar](https://collerek.github.io/ormar/)                                                  | `fastapi_pagination.ext.ormar.paginate`             |\n| [Piccolo](https://piccolo-orm.readthedocs.io/en/latest/)                                    | `fastapi_pagination.ext.piccolo.paginate`           |\n| [PyMongo](https://pymongo.readthedocs.io/en/stable/)                                        | `fastapi_pagination.ext.pymongo.paginate`           |\n| [Tortoise ORM](https://tortoise-orm.readthedocs.io/en/latest/)                              | `fastapi_pagination.ext.tortoise.paginate`          |\n\n\n---\n\nCode from `Quickstart` will generate OpenAPI schema as bellow:\n\n<div align="center">\n<img alt="app-example" src="docs/img/example.jpeg">\n</div>\n',
    'author': 'Yurii Karabas',
    'author_email': '1998uriyyo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/uriyyo/fastapi-pagination',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
