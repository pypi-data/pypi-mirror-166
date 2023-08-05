# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['websockets_actions',
 'websockets_actions.broadcast',
 'websockets_actions.fastapi',
 'websockets_actions.starlette']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'websockets-actions',
    'version': '0.3.1',
    'description': 'Using Actions for Websockets',
    'long_description': '# WebSocket Actions\n\nНадстройка над Starlette, FastAPI для более удобной работы с WebSockets.\n\n## Установка\n\n```shell\n$ pip install wensockets-actions\n```\n\n\n## Пример\n\n**example.py**:\n\n```python\n\n```\n\nЗапустить приложение...\n\n```shell\n$ uvicorn example:app\n```\n\nБольше примеров, [здесь]().\n',
    'author': 'Omelchenko Michael',
    'author_email': 'socanime@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DJWOMS/websockets-actions',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
