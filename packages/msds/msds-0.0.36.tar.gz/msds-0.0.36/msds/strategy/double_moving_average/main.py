import numpy as np

# 策略回测方法
def test(df, para):
    '''
    输入: df是k线数据、para是策略的参数
    策略: white your backtest code here
    '''

    df['signal'] = None
    return df

# 策略回测参数
def testParam(m_list = range(10, 1000, 10), n_list = [i / 10 for i in list(np.arange(5, 50, 1))]):
    # 1、单参数类型，返回单个数组数据
    para = [150, 270, 0.2, 0.1]
    return para

    # 2、多参数类型, 返回多个数据的数组
    for m in m_list:
        for n in n_list:
            para = [m, n]
            para_list.append(para)
    return para_list

# 策略实盘方法
def strategy(df, para):
    '''
    输入: df是k线数据、para是策略的参数
    策略: white your firm offer code here
    '''

    signal = None
    return signal

# 策略实盘参数
def strategyParam(df, para):
    return [150, 270, 0.2, 0.1]
