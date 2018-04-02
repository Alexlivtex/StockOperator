#from module_utility.LearningMarketsToturial.obtain_video_list import get_video_link
#from module_utility.LearningMarketsToturial.video_download import download_video
from module_utility.StockDataObtain.get_stock_ticker import fetch_stock_symbol
from module_utility.StockDataObtain.stockcharts_obtain import grab_data_from_stockcharts
from module_utility.StockDataObtain.indicator_caculation import caculate_indicator
from module_utility.StockDataObtain.score_calculation import calc_score
from time import sleep
import pandas as pd
import numpy as np
import shutil
import glob
import os
import math
import threading
import schedule
import time
import json

need_update = False
STOCK_TICKER_PATH = os.path.join("data", "StockData", "TickerSymbol", "Stock")
STOCK_DATA_PATH = os.path.join("data", "StockData", "Stock")
STOCK_JSON_PATH = os.path.join("config", "StockOperation", "config.json")
max_thread_count = 2

def list_chunks(ticker_list, sub_count):
    sub_count = int(sub_count)
    for i in range(0, len(ticker_list), sub_count):
        yield ticker_list[i:i + sub_count]

def main():

    stock_list = []
    threads_complte = []

    #1:Get video link from learning makets
    #get_video_link()

    #2:Get learning markets video
    #download_video()

    #3:Get latest stock data
    f = open(STOCK_JSON_PATH, "r")
    data = json.load(f)
    operation_times = int(data["operation_times"])
    f.close()

    data["operation_times"] = str(int(data["operation_times"]) + 1)
    if data["stockcharts"][0]["id"] == "XXXXXXX" or data["stockcharts"][0]["password"] == "XXXXXXX":
        print("Please input the account :")
        data["stockcharts"][0]["id"] = input()
        print("Please input the password :")
        data["stockcharts"][0]["password"] = input()

    f = open(STOCK_JSON_PATH, "w")
    f.write(json.dumps(data, ensure_ascii=False, indent=4, separators=(",", ":")))
    f.close()

    if operation_times % 30 == 0:
        fetch_stock_symbol()
    else:
        print("Stock symbol no need to update!!!")

    for data in glob.glob("stocks.*"):
        print(data)
        shutil.move(data, os.path.join(STOCK_TICKER_PATH, data))

    if os.path.exists(STOCK_DATA_PATH):
        shutil.rmtree(STOCK_DATA_PATH)

    os.mkdir(STOCK_DATA_PATH)

    
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

    
    #4:Caculate the tec indicator for stock quote
    for stock_item in os.listdir(STOCK_DATA_PATH):
        if stock_item.split(".")[-1] == "csv":
            df = pd.read_csv(os.path.join(STOCK_DATA_PATH, stock_item))
            open_price = np.asarray(df["Open"])
            if len(open_price) < 400:
                print("===================Data length not enough!==================")
                os.remove(os.path.join(STOCK_DATA_PATH, stock_item))
                continue

            caculate_indicator(os.path.join(STOCK_DATA_PATH, stock_item))
            calc_score(os.path.join(STOCK_DATA_PATH, stock_item))
            os.remove(os.path.join(STOCK_DATA_PATH, stock_item))
            print("{} transform finished".format(stock_item))

#schedule.every().day.at("07:00").do(main)
#while True:
#    schedule.run_pending()
main()
