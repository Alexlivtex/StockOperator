import os
import pickle
import requests
import youtube_dl
from bypy import ByPy
import shutil
from check_disk_status import check_disk_percentage

video_data_dic = dict()
item_link_list = list()

finished_list = list()

video_data_pickle = os.path.join("config", "LearningMarketsToturial","video_data.pickle")
video_data_pickle_bak = os.path.join("config", "LearningMarketsToturial","video_data_bak.pickle")

finished_pickle = os.path.join("config", "LearningMarketsToturial","finished_downloading.pickle")
finished_pickle_bak = os.path.join("config", "LearningMarketsToturial","finished_downloading_bak.pickle")

video_download_path = os.path.join("data", "LearningMarketsVideo")

MAX_DOWNLOAD_COUNT = 5

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
    global finished_list

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

    if os.path.exists(finished_pickle):
        try:
            f_finished_data = open(finished_pickle, "rb")
            finished_list = pickle.load(f_finished_data)
            f_finished_data.close()
        except:
            try:
                f_finished_data = open(finished_pickle_bak, "rb")
                finished_list = pickle.load(f_finished_data)
                f_finished_data.close()
            except:
                print("Both data file not exists, just leave it empty!")
                return

    current_download_count = 0
    for dic_index in video_data_dic:
        if dic_index in finished_list:
            continue
        percent = check_disk_percentage()
        if percent > 0.7:
            print("Disk space nearly full, exist")
            if os.listdir(video_download_path):
                bp = ByPy()
                bp.upload("data")
                bp.cleancache()
                shutil.rmtree(video_download_path)
                os.mkdir(video_download_path)
            return
        else:
            if current_download_count % MAX_DOWNLOAD_COUNT == 0:
                bp = ByPy()
                bp.upload("data")
                bp.cleancache()
                shutil.rmtree(video_download_path)
                os.mkdir(video_download_path)

            file_name = os.path.join(video_download_path, video_data_dic[dic_index][0])
            video_link = video_data_dic[dic_index][1]
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': file_name
            }

            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_link])

                finished_list.append(dic_index)
                f_finished_data = open(finished_pickle, "wb")
                pickle.dump(finished_list, f_finished_data)
                f_finished_data.close()
                shutil.copy(finished_pickle, finished_pickle_bak)
                current_download_count += 1
            except:
                print("{} seems has an error in it".format(video_link))
                continue
