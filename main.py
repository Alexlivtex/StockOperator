from module_utility.LearningMarketsToturial.obtain_video_list import get_video_link
from module_utility.LearningMarketsToturial.video_download import download_video
from module_utility.StockDataObtain.get_stock_ticker import fetch_stock_symbol

def main():
    get_video_link()
    download_video()
    fetch_stock_symbol()

main()
