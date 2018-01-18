import os

def fetch_stock_symbol():
    os.system("YahooTickerDownloader.py stocks -m us")
    os.system("YahooTickerDownloader.py stocks -m us --export")
