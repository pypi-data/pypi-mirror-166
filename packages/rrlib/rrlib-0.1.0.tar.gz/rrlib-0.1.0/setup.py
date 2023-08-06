# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['rrlib']
setup_kwargs = {
    'name': 'rrlib',
    'version': '0.1.0',
    'description': 'Chatbot request and response tool',
    'long_description': 'Request-Response Library\n\nПрограмма позволяет работать с библиотеками запросов-ответов для чат-ботов и виртуальных ассистентов.\n',
    'author': 'exerussus',
    'author_email': 'solovyov.production@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
