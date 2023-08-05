# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['shiki4py', 'shiki4py.resources', 'shiki4py.store', 'shiki4py.types']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'attrs>=22.1.0,<23.0.0',
 'cattrs>=22.1.0,<23.0.0',
 'pyrate-limiter>=2.8.1,<3.0.0',
 'python-dotenv>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'shiki4py',
    'version': '2.1.0',
    'description': 'Asynchronous client for api Shikimori written in Python 3.7 with asyncio and aiohttp.',
    'long_description': '<p align="center">\n  <img src="./assets/shiki4py_logo.svg" alt="Shiki4py" width="35%">\n</p>\n\n<p align="center">\n  <a href="https://github.com/ren3104/Shiki4py/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/ren3104/Shiki4py"></a>\n  <a href="https://pypi.org/project/shiki4py"><img src="https://img.shields.io/pypi/v/shiki4py?color=blue" alt="PyPi package version"></a>\n  <a href="https://pypi.org/project/shiki4py"><img src="https://img.shields.io/pypi/pyversions/shiki4py.svg" alt="Supported python versions"></a>\n</p>\n\nАсинхронный клиент для взаимодействия с [api Shikimori](https://shikimori.one/api/doc/1.0), написанный на Python 3.7 c использованием [asyncio](https://docs.python.org/3/library/asyncio.html) и [aiohttp](https://github.com/aio-libs/aiohttp).\n\nВерсии shiki4py v0.2.2 и раньше являются синхронными, но начиная с v2.0.0 этот пакет стал асинхронным. Рекомендую использовать в своих проектах только shiki4py >= v2.0.0!\n\nСравнение shiki4py v0.2.2 и v2.0.0 по времени отправки 25 запросов:\n\n<img src="https://raw.githubusercontent.com/ren3104/Shiki4py/main/assets/sync_vs_async.svg" alt="Shiki4py sync vs async" width="500">\n\nshiki4py v0.2.2 ~10.5 секунд\n<details>\n<summary>Код</summary>\n\n```python\nfrom shiki4py import Client\n\n\nclient = Client("APP_NAME",\n                "CLIENT_ID",\n                "CLIENT_SECRET")\nfor i in range(25):\n    client.get(f"/users/{i}/info")\n```\n</details>\n\nshiki4py v2.0.0 ~5.07 секунд\n<details>\n<summary>Код</summary>\n\n```python\nfrom shiki4py import Shikimori\nimport asyncio\n\n\nasync def main():\n    async with Shikimori("APP_NAME", "CLIENT_ID", "CLIENT_SECRET") as api:\n        await asyncio.gather(*[api.users.info(i) for i in range(25)])\n\n\nasyncio.run(main())\n```\n</details>\n\n## Особенности\n* Поддержка api v1 и v2\n* Ограничения 5rps и 90rpm\n* OAuth2 авторизация\n* Контроль срока действия токена\n* Хранение токенов в `.env` файле\n* Свой класс с методами для каждого ресурса api (пока только для `comments` и `users`)\n* Представление json данных как python классы\n\n## Установка\n```bash\npip install shiki4py\n```\n\n## Использование\n### Быстрый старт\n```python\nfrom shiki4py import Shikimori\nimport asyncio\nimport logging\n\n\nlogging.basicConfig(level=logging.INFO)\n\n\nasync def main():\n    # Клиент без авторизации\n    async with Shikimori("APP_NAME") as api:\n        clubs = await api.users.clubs(555400)\n        print(clubs)\n\n    # Клиент с авторизацией\n    api = Shikimori("APP_NAME",\n                    "CLIENT_ID",\n                    "CLIENT_SECRET")\n    await api.open()\n    # Отправляем запросы\n    # await api.client.request(...)\n    # await api.users.favourites(...)\n    # await api.comments.show_one(...)\n    # ...\n    await api.close()\n\n\nasyncio.run(main())\n```\n### Сохранение токенов авторизации\nПо умолчанию клиент сохраняет токены авторизации в файле .env, но при инициализации можно выбрать другой вариант хранения токенов, либо создать свой вариант унаследовав базовый класс и переопределив его методы.\n```python\nfrom shiki4py import Shikimori\nfrom shiki4py.store import BaseTokenStore\nfrom shiki4py.store.memory import MemoryTokenStore\n\n\nclass MyTokenStore(BaseTokenStore):\n    ...\n\n\napi = Shikimori("APP_NAME",\n                "CLIENT_ID",\n                "CLIENT_SECRET",\n                # store=MyTokenStore()\n                store=MemoryTokenStore())\n```\n\n## Зависимости\n* [aiohttp](https://github.com/aio-libs/aiohttp) - для асинхронных http запросов\n* [PyrateLimiter](https://github.com/vutran1710/PyrateLimiter) - для ограничения частоты запросов\n* [attrs](https://github.com/python-attrs/attrs) - для преобразования данных json в python классы\n* [cattrs](https://github.com/python-attrs/cattrs) - дополнение к attrs для структурирования и деструктурирования данных\n* [python-dotenv](https://github.com/theskumar/python-dotenv) - для сохранения токенов авторизации в `.env` файл\n',
    'author': 'ren3104',
    'author_email': '2ren3104@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ren3104/Shiki4py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
