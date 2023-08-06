# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['smpljson']
setup_kwargs = {
    'name': 'smpljson',
    'version': '0.1.0',
    'description': 'A simple module for reading and writing JSON',
    'long_description': '\nJSON Operations\n\nA simple module for reading and writing JSON.\nFunctions:\n1. read - returns the value of the JSON file;\n2. save - saves the value of a variable in a JSON file.\n\n\nПростой модуль для чтения и записи JSON-файлов.\n1. read - возвращает значение JSON-файла;\n2. save - экспортирует значение переменной в JSON-файл.\n',
    'author': 'exerussus',
    'author_email': 'solovyov.production@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
