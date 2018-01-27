from selenium import webdriver
from bs4 import BeautifulSoup
from check_disk_status import check_disk_percentage
import urllib2
import os
import pickle
import shutil

video_data_dic = dict()
item_link_list = list()
video_data_pickle = os.path.join("config", "LearningMarketsToturial","video_data.pickle")
video_data_pickle_bak = os.path.join("config", "LearningMarketsToturial","video_data_bak.pickle")

video_download_path = os.path.join("data", "LearningMarketsVideo")

def write_data(data, file, bak_file):
    f_video_data = open(file, "wb")
    pickle.dump(data, f_video_data)
    f_video_data.close()
    shutil.copy(file, bak_file)

def get_video_link():
    global video_data_dic
    global item_link_list

    if os.path.exists(video_data_pickle):
        try:
            f_video_data = open(video_data_pickle, "rb")
            video_data_dic = pickle.load(f_video_data)
            f_video_data.close()
        except:
            try:
                f_video_data = open(video_data_pickle_bak, "rb")
                video_data_dic = pickle.load(f_video_data)
                f_video_data.close()
            except:
                print("Both data file not exists, just leave it empty!")

    #driver = webdriver.Firefox()
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome("/usr/bin/chromedriver",chrome_options=options)
    driver.get("https://www.learningmarkets.com/strategy-sessions/")
    buttont_elem = driver.find_element_by_css_selector(".btn.btn-default.dropdown-toggle")
    buttont_elem.click()

    li_list = driver.find_elements_by_css_selector(".dropdown-item.dropdown-item-button")
    for li_item in li_list:
        if li_item.text == "All":
            li_item.click()
            break

    link_list = driver.find_elements_by_tag_name("a")
    for item_index in link_list:
        if item_index.text == "view":
            item_url = item_index.get_attribute("href")[:-1]
            item_link_list.append(item_url)

    driver.close()

    for link_item in item_link_list:
        if link_item in video_data_dic:
            print("{} has already existed!".format(link_item))
            continue
        else:
            soup = BeautifulSoup(urllib2.urlopen(link_item), "html5lib")
            video_link = soup.find_all("source")[0]["src"]
            # print(video_link)
            file_name = link_item.split("/")[-1] + ".mp4"
            originan_name = file_name
            url = video_link[:-4]
            original_file_name = url.split("/")[-1]
            original_file_name = original_file_name.split(".")[0]
            year = original_file_name.split("-")[-2]
            month = original_file_name.split("-")[0][2:]
            day = original_file_name.split("-")[1]
            time_stap = year + "-" + month + "-" + day + "-"
            file_name = time_stap + file_name
            print(file_name)
            print(url)
            video_data_dic[link_item] = [file_name, url]
            if len(video_data_dic) % 20 == 0:
                write_data(video_data_dic, video_data_pickle, video_data_pickle_bak)

    write_data(video_data_dic, video_data_pickle, video_data_pickle_bak)
    del video_data_dic
    del item_link_list
