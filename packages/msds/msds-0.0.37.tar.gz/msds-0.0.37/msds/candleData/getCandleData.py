import os
import pandas as pd;
from time import sleep
from math import ceil
from rich import print
from rich.status import Status
from rich.progress import Progress
from msds.base.request import getOhlcv
from msds.base.data import dataClean
from msds.base.util import makedirs, getIntervalSeconds, getExchangeInstance
from msds.config.config import EXCHANGE_LIMIT, CANDLE_DATA_COL_NAME

pd.set_option('expand_frame_repr', False)

def save_spot_candle_data_from_exchange(exchange, symbol, start_time_string, end_time_string, time_interval):
    exchangeInstance = getExchangeInstance(exchange)

    print('[bold green]【数据配置】：[/bold green]通过 '+exchange+' 来请求 '+start_time_string+' 到 '+end_time_string+' 之间的 '+symbol+' '+time_interval+' 的数据')

    # 时间定义：将时间字符串转为时间对象、毫秒时间戳
    end_time = pd.to_datetime(end_time_string) # eg. 2022-07-30 00:00:00
    start_time = pd.to_datetime(start_time_string) # eg. 2020-05-01 00:00:00
    end_time_stamp_ms =  exchangeInstance.parse8601(end_time_string) # eg. 1659139200000
    start_time_stamp_ms = exchangeInstance.parse8601(start_time_string) # eg. 1588291200000

    # 变量定义
    df_list = []
    process_length = ceil((((end_time_stamp_ms - start_time_stamp_ms) / 1000) / getIntervalSeconds(time_interval)) / 500)

    # 请求数据
    with Progress() as progress:
        task1 = progress.add_task('[bold green]【下载进度】: ', total=process_length)
        while True:
            try:
                df_item = getOhlcv(exchangeInstance, symbol, time_interval, start_time_stamp_ms, EXCHANGE_LIMIT[exchangeInstance.id])
            except Exception as Argument:
                progress.update(task1, visible=False)
                print('[bold red]【请求失败】: [/bold red]请检查网络和参数后重试')
                print('[bold red]【错误原因】: [/bold red]', Argument)
                return
            # 格式处理
            df_item = pd.DataFrame(df_item, dtype=float)
            df_list.append(df_item)
            progress.update(task1, advance=1)

            # 分页判断
            df_item_time = pd.to_datetime(df_item.iloc[-1][0], unit='ms')
            start_time_stamp_ms = exchangeInstance.parse8601(str(df_item_time))
            if df_item_time >= end_time or df_item.shape[0] <= 1:
                progress.update(task1, visible=False)
                break
            sleep(1)

    with Status('数据处理: 开始') as status:
        status.update('数据合并处理中')
        df = pd.concat(df_list, ignore_index=True)
        df[0] = pd.to_datetime(df[0], unit='ms')
        df.rename(columns=CANDLE_DATA_COL_NAME, inplace=True)
        df = dataClean(df)
        df = df[(df['candle_begin_time'] >= start_time) & (df['candle_begin_time'] < end_time)]

        status.update('创建文件：系统实际存储文件夹、文件')
        dataNameDir = '{}/{}/{}/{}'.format(
            exchangeInstance.id,
            symbol.replace('/', '-'),
            time_interval,
            str(start_time.date())+'_'+str(end_time.date())
        )
        dataNameFile = dataNameDir.replace('/', '_')

        absolute_path = os.path.join(os.getcwd(), '__dacache__/' + dataNameDir)
        makedirs(absolute_path)
        df.to_csv(os.path.join(absolute_path, dataNameFile + '.csv'), index=False)
        df.to_hdf(os.path.join(absolute_path, dataNameFile + '.h5'), key="df", mode="w", index=False)
        status.update(None)
        print('[bold green]【存储成功】: [/bold green]' + absolute_path)
