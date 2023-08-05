# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pynoticenter']

package_data = \
{'': ['*']}

install_requires = \
['asyncio>=3.4.3,<4.0.0']

entry_points = \
{'console_scripts': ['demo = src.example.demo:main']}

setup_kwargs = {
    'name': 'pynoticenter',
    'version': '0.1.1',
    'description': 'Python client side notification center.',
    'long_description': 'PyNotiCenter Documentation\n==========================\n\n[![Docs](https://img.shields.io/badge/docs-latest-informational)](https://dzhsurf.github.io/pynoticenter/)\n\n## Introduction\n\nPython client side notification center.\n\n## Install\n\n```shell\npip install pynoticenter\n```\n\n## Code Example\n\n```python\ndef fn(*args: Any, **kwargs: Any):\n    print(*args)\n\ndef main():\n    PyNotiCenter.default_center().post_task(fn, "hello world")\n    PyNotiCenter.default_center().post_task_with_delay(5, fn, "hello", "world", "delay 5s")\n    PyNotiCenter.default_center().shutdown(wait=True)\n```\n\n```shell\n[2022-09-03 20:54:23,698] {task_queue.py:177} INFO - TaskQueue[4408264928]: worker thread begin.\n[2022-09-03 20:54:23,699] {task_queue.py:46} INFO - TaskQueue[4408264928]: Task queue terminate. wait: True\n[2022-09-03 20:54:23,699] {task_queue.py:105} INFO - TaskQueue[4408264928]: waiting for tasks cleanup. tasks: 2\nhello world\nhello world delay 5s\n[2022-09-03 20:54:28,721] {task_queue.py:114} INFO - TaskQueue[4408264928]: All tasks cleanup. wait time: 5.0\n[2022-09-03 20:54:28,722] {task_queue.py:117} INFO - TaskQueue[4408264928]: waiting for thread exit.\n[2022-09-03 20:54:28,722] {task_queue.py:137} INFO - TaskQueue[4408264928]: stop event run loop.\n[2022-09-03 20:54:28,723] {task_queue.py:200} INFO - TaskQueue[4408264928]: worker thread end.\n[2022-09-03 20:54:29,726] {task_queue.py:126} INFO - TaskQueue[4408264928]: thread exit. wait time: 1.0\n```',
    'author': 'dzhsurf',
    'author_email': 'dzhsurf@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dzhsurf/pynoticenter',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
