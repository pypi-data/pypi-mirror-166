import os, shutil, re, ccxt, sys
from rich import print

# 递归创建文件夹
def makedirs(path):
    if os.path.exists(path) is False: 
        os.makedirs(path)

# 获取时间周期的秒数
def getIntervalSeconds(s):
    timeMap = {
        'm': 60,
        'h': 60 * 60,
        'd': 60 * 60 * 24
    }
    regResult = re.findall(r'[0-9]+|[a-z]+', s)
    seconds = int(regResult[0]) * int(timeMap[regResult[1]])
    return seconds

# 获取交易所实例
def getExchangeInstance(s):
    if s == 'binance':
        return ccxt.binance()
    if s == 'okx':
        return ccxt.okx()
    if s == 'huobi':
        return ccxt.huobi()

# 将某文件夹下所有的文件&文件夹，复制到另外一个目标文件夹内
def dirCopy(src, des):
    src = os.path.normpath(src)
    des = os.path.normpath(des)

    if not os.path.exists(src) or not os.path.exists(src):
        print("[bold red]创建失败: 源配置文件夹不存在[/bold red]: ", src)
        sys.exit(1)

    #获得原始目录中所有的文件，并拼接每个文件的绝对路径
    os.chdir(src)

    src_file_list = [os.path.join(src, file) for file in os.listdir()]
    target_file_list = [os.path.join(des, file) for file in os.listdir()]

    for index in range(len(src_file_list)):
        if os.path.exists(target_file_list[index]):
            continue

        if os.path.isfile(src_file_list[index]):
            shutil.copy(src_file_list[index], des)
            print('[bold green]创建文件成功: ' + target_file_list[index] + '[/bold green]')

        if os.path.isdir(src_file_list[index]):
            p, src_name = os.path.split(src_file_list[index])
            shutil.copytree(src_file_list[index], os.path.join(des, src_name))
            print('[bold green]创建文件夹成功: ' + target_file_list[index] + '[/bold green]')