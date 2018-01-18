from module_utility.LearningMarketsToturial.obtain_video_list import get_video_link
from module_utility.LearningMarketsToturial.video_download import download_video
from module_utility.StockDataObtain.get_stock_ticker import fetch_stock_symbol
from module_utility.StockDataObtain.stockcharts_obtain import grab_data_from_stockcharts
from time import sleep
import pandas as pd
import numpy as np
import shutil
import glob
import os
import math
import threading

need_update = False
STOCK_TICKER_PATH = os.path.join("data", "StockData", "TickerSymbol", "Stock")
STOCK_DATA_PATH = os.path.join("data", "StockData", "Stock")
max_thread_count = 2

def list_chunks(ticker_list, sub_count):
    sub_count = int(sub_count)
    for i in range(0, len(ticker_list), sub_count):
        yield ticker_list[i:i + sub_count]

def main():
    stock_list = []
    threads_complte = []

    get_video_link()
    download_video()
    if need_update:
        fetch_stock_symbol()

    for data in glob.glob("stocks.*"):
        print(data)
        shutil.move(data, os.path.join(STOCK_TICKER_PATH, data))

    stock_data = pd.read_csv(os.path.join(STOCK_TICKER_PATH, "stocks.csv"))
    stock_data = stock_data.loc[stock_data["Exchange"].isin(['NYQ', 'NMS'])]
    print(stock_data["Ticker"])
    print(np.array(stock_data["Ticker"]))
    print(np.array(stock_data["Ticker"]).tolist())
    stock_list.extend(np.array(stock_data["Ticker"]).tolist())
    final_list_complete = list(list_chunks(stock_list, math.ceil(len(stock_list) / max_thread_count)))
    print(final_list_complete)

    for i in range(max_thread_count):
        threads_complte.append(threading.Thread(target=grab_data_from_stockcharts, args=(STOCK_DATA_PATH, final_list_complete[i])))

    for t in threads_complte:
        t.setDaemon(True)
        sleep(10)
        t.start()

    for thread_index in threads_complte:
        thread_index.join()
main()
