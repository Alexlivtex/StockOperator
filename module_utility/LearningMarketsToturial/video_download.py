import os
import pickle
import requests
import youtube_dl
from check_disk_status import check_disk_percentage

video_data_dic = dict()
item_link_list = list()
video_data_pickle = os.path.join("config", "LearningMarketsToturial","video_data.pickle")
video_data_pickle_bak = os.path.join("config", "LearningMarketsToturial","video_data_bak.pickle")

video_download_path = os.path.join("data", "LearningMarketsVideo")

def as_num(x):
    y='{:.5f}'.format(x)
    return(y)

def download_file(url, file_name):
    r = requests.get(url, stream=True)
    total_size = requests.head(url).headers['content-length']
    current_download_index = 0
    with open(file_name, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                current_download_index += 1
                if current_download_index % (1024*5) == 0:
                    download_percent = (current_download_index * 1024) / float(total_size)
                    print("{} has already downloaded {}".format(file_name, str(download_percent * 100)[:6] + "%"))
    print("{} has already downloaded {}".format(file_name, str(100) + "%"))
    f.close()

def download_video():
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
                return

    for dic_index in video_data_dic:
        percent = check_disk_percentage()
        if percent > 0.7:
            print("Disk space nearly full, exist")
        else:
            file_name = os.path.join(video_download_path, video_data_dic[dic_index][0])
            video_link = video_data_dic[dic_index][1]
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': file_name
            }

            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_link])
            except:
                print("{} seems has an error in it".format(video_link))
                continue

download_video()
