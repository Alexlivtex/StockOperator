import requests
import bs4 as bs
import time
import os
import pickle
import shutil

def extract_ticker_list(parameList):
    url = parameList["fz_url"]
    data = parameList["ticker_data"]
    data_bak = parameList["ticker_data_bak"]

    page_index = 1
    if os.path.exists(data):
        with open(data, "rb") as f:
            ticker_list = pickle.load(f)
    else:
        ticker_list = list()

    hasNextPage = True
    while hasNextPage:
        ticker_screen_url = url + "/screener.ashx?v=111&r=" + str((page_index - 1) * 2) + "1"
        response = requests.get(ticker_screen_url)
        soup = bs.BeautifulSoup(response.content, "lxml")
        print(ticker_screen_url)

        if len(soup.find_all("b", string="next")) > 0:
            hasNextPage = True
        else:
            hasNextPage = False

        for item in soup.find_all("a", {"class" : "screener-link-primary"}):
            print(item.text)
            if not item.text in ticker_list:
                ticker_list.append(item.text)

        with open(data, "wb") as f:
            pickle.dump(ticker_list, f)

        shutil.copy(data, data_bak)
        page_index += 1
        time.sleep(2)

    print("*****************Total ticker count is {}*****************".format(len(ticker_list)))

