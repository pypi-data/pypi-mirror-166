# -*- coding:utf-8 -*-
"""
Author: Wdataorg
Date: .09.04
Project Name: Wdata
"""
from setuptools import setup
from cnforpy.version import __VERSION__

def read(filename: str) -> str:
    with open(filename, 'r+', encoding='utf-8') as file:
        return file.read()

NAME = "cnforpy"
VERSION = __VERSION__
AUTHOR = 'Leaves-Technology'
AUTHOR_EMAIL = "rainwang_20220102@163.com"
MAINTAINER = 'Leaves-Technology'
MAINTAINER_EMAIL = "rainwang_20220102@163.com"
URL = "https://heikeling.github.io"
DESCRIPTION = '一个中文编程语言'
LONG_DESCRIPTION = '\n'.join([DESCRIPTION, read('README.md')])
REQUIREMENTS = [
                'setuptools==62.3.4',
                'easygui==0.98.3',
                'requests==2.28.0'
                ]
PACKAGES = ["cnforpy"]
python_requires = '>=3.8'
LICENSE = read('LICENSE')

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    url=URL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    install_requires=REQUIREMENTS,
    packages=PACKAGES,
    long_description_content_type='text/markdown',
    classifiers=[
            'Environment :: Console',
            'Natural Language :: Chinese (Simplified)',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: Implementation',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Operating System :: OS Independent'
        ],
    python_requires=python_requires,
    license=LICENSE,
    entry_points={
            'console_scripts': [
                'cnforpy = cnforpy:main'
            ]
        }
)