import json
import os

def check_env():
    modules = ["selenium", "beautifulsoup4", "pandas", "requests"]
    for module in modules:
        try:
            __import__(module)
            print("{} has already installed".format(module))
            os.system("pip install -U {}".format(module))
        except ImportError:
            print("{} can not be found".format(module))
            #subprocess.call("pip install {}".format(module))
            os.system("pip install {}".format(module))


check_env()

from module_utility.ticker_obtain.finviz_source import extract_ticker_list
from module_utility.stock_data_obtain.sc_stock_obtain import grab_data_from_stockcharts

def loadConfig(configPath):
    with open(configPath, "r") as f:
        paramList = json.load(f)
        if(paramList["config_data"] == "config.json"):
            paramList["config_data"] = os.path.join("config", "config.json")

        if paramList["ticker_data"] == "ticker.pickle":
            paramList["ticker_data"] = os.path.join(os.path.join("data", "ticker"), paramList["ticker_data"])

        if paramList["ticker_data_bak"] == "ticker_bak.pickle":
            paramList["ticker_data_bak"] = os.path.join(os.path.join("data", "ticker"), paramList["ticker_data_bak"])

        if paramList["stock_data"] == "stock.pickle":
            paramList["stock_data"] = os.path.join(os.path.join("data", "stock", "extract_data"), paramList["stock_data"])

        if paramList["stock_data_bak"] == "stock_bak.pickle":
            paramList["stock_data_bak"] = os.path.join(os.path.join("data", "stock", "extract_data"), paramList["stock_data_bak"])

        if paramList["stock_data_path"] == "":
            paramList["stock_data_path"] = os.path.join("data", "stock", "stock_data")

        if paramList["fz_url"] == "":
            paramList["fz_url"] = input("Please input the fz_url to get ticker : ")

        if paramList["sc_url"] == "":
            paramList["sc_url"] = input("Please input the sc_url to get data : ")

        if paramList["sc_user_name"] == "":
            paramList["sc_user_name"] = input("Please input the sc username : ")

        if paramList["sc_user_password"] == "":
            paramList["sc_user_password"] = input("Please input the sc password : ")

        paramList["fz_url"] = paramList["fz_url"].strip()
        paramList["sc_url"] = paramList["sc_url"].strip()

        if paramList["fz_url"][-1] == '/':
            paramList["fz_url"] = paramList["fz_url"][:-1]

        if paramList["sc_url"][-1] == '/':
            paramList["sc_url"] = paramList["sc_url"][:-1]

    with open(configPath, "w") as f:
        json.dump(paramList, f, ensure_ascii=False, indent=4, separators=(",", ":"))

    return paramList

def main():
    config_path = os.path.join("config", "config.json")
    paramList = loadConfig(config_path)

    extract_ticker_list(paramList)
    grab_data_from_stockcharts(paramList)

main()
