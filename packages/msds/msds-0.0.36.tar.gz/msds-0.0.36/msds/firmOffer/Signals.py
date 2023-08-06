import pandas as pd
import random

# 双均线实盘交易信号
def real_signal_simple_double_moving_average(
    df,
    para,
    currentPos,
    currentHoldPrice
):

    # ===策略参数
    # s 代表短线长度
    # l 代表长线长度
    # m 代表上轨标准差的倍数
    # n 代表下轨标准差的倍数
    s = int(para[0])
    l = int(para[1])
    m = para[2]
    n = para[3]
    # ru = para[3]
    # rl = para[4]

    # ===计算指标
    # 计算双均线
    df['short'] = df['close'].ewm(adjust=False, span=s).mean()
    short = df.iloc[-1]['short']

    df['long'] = df['close'].rolling(l, min_periods=1).mean()
    long = df.iloc[-1]['long']

    # 计算标准差
    df['std'] = df['close'].rolling(l, min_periods=1).std(ddof=0)
    std = df.iloc[-1]['std']

    close = df.iloc[-1]['close']

    # 计算上轨、下轨道
    upper = long + m * std
    lower = long - n * std

    # ===寻找交易信号
    signal = None

    # 找出做多信号
    if short > upper:
        signal = 1
    # 找出做空信号
    elif short < lower:
        signal = -1

    # 叠加计算双向止盈条件
    # priceGap = (close - currentHoldPrice) / currentHoldPrice
    # if ((currentPos == 1) & (priceGap > ru) & (short < upper)):
    #    signal = 0
    # elif ((currentPos == -1) & (priceGap < -rl) & (short > lower)):
    #    signal = 0
  
    return signal