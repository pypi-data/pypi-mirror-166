#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
路径: PATH_ROOT: 当前msds主包__init__.py所处的位置上一层
作用: 将该路径加入到系统路径中, 保证其它的python文件能够互相通过模块的方式引入
注意: 当全局安装了msds这个包, 但是通过开发的方式运行当前文件时, 其它文件使用模块引入时, 会优先选择引入的是全局的模块
'''
import os
import sys
PATH_ROOT = os.path.join(sys.path[0], '../')
sys.path.append(PATH_ROOT)

import click
import importlib
import configparser
from rich import print
from msds.base.path import PATH_SOURCE
from msds.base.util import dirCopy
from msds.backTest.getBackTest import go_back_test
from msds.candleData.getCandleData import save_spot_candle_data_from_exchange
from msds.website.flask import create_app

'''
作用: 读取代码实际运行时（使用工具的人执行时）路径下的配置文件
'''
config = configparser.ConfigParser()
config.read([os.path.join(os.getcwd(), 'main.ini')])

# ------------------------------ 命令定义 ------------------------------
@click.group()
def msds():
    pass

@msds.command()
def init():
    dirCopy(
        os.path.join(PATH_SOURCE, 'msds/base/__initial__'),
        os.getcwd()
    )

@msds.command()
def data():
    candleConfig = config['CANDLE_DATA']
    return save_spot_candle_data_from_exchange(
        candleConfig['exchange'],
        candleConfig['symbol'],
        candleConfig['time_start'],
        candleConfig['time_end'],
        candleConfig['time_interval']
    )

@msds.command()
def backtest():
    if not bool(config.has_section('BACK_TEST_DATA') and config.has_section('BACK_TEST_SYMBOL')):
        return

    # 策略文件引入
    sys.path.append(os.getcwd())
    strategy = importlib.import_module('main')

    go_back_test(
        strategy,
        config['BACK_TEST_DATA'],
        config['BACK_TEST_SYMBOL']
    )

@msds.command()
def website():
    myFlaskApp = create_app()
    myFlaskApp.run()

@msds.command()
def test():
    print('This is a test command ~')
    return

# ------------------------------ 服务入口 ------------------------------

def entry():
    msds()

# 描述: 只有脚本执行的方式时运行main函数
# case1、当该模块被直接执行时: __name__ 等于文件名（包含后缀 .py ）
# case2、当该模块 import 到其他模块中:  __name__ 等于模块名称（不包含后缀.py）
if __name__ == '__main__':
    entry()
