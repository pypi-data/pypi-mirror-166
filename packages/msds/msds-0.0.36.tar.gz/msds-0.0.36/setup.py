#!usr/bin/env python
# -*- coding:utf-8 _*-

"""
@author:    Nundy
@file:      setup.py
@time:      2022/06/28
@desc:      梅赛德斯车主
"""

# 版本管理
VERSION = '0.0.36'

# 构建依赖
INSTALL_REQUIRES = [
    'pandas',
    'tenacity',
    'inquirer',
    'click',
    'rich',
    'tables',
    'ccxt',
    'numpy',
    'Flask',
    'twine',
    'setuptools'
]

from setuptools import setup, find_packages

# 配置导出
setup(
    name = 'msds',
    version = VERSION,
    url = 'https://gitee.com/dawajituan',
    description = 'msds tools',
    author = 'Nundy',
    author_email = '18710939328@163.com',
    license = 'MIT',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    install_requires = INSTALL_REQUIRES,
    python_requires = '>=3.7.8',
    entry_points={
        'console_scripts': [
            'msds = msds:entry'
        ]
    }
)
