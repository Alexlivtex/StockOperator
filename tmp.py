# -*- coding:utf-8 -*-

from uiautomator import Device
import random
import pickle

import time

import os
import io

ENG_DEVICE_ID = "3204928f588f1157"
CHN_DEVICE_ID = "2646acdf"

d_eng = Device(ENG_DEVICE_ID)
print(d_eng.info)

d_chn = Device(CHN_DEVICE_ID)
print(d_chn.info)




def input_date(date_time, ID):
    options_map = {"1": "Jan",
                   "2": "Feb",
                   "3": "Mar",
                   "4": "Apr",
                   "5": "May",
                   "6": "Jun",
                   "7": "Jul",
                   "8": "Aug",
                   "9": "Sep",
                   "10": "Oct",
                   "11": "Nov",
                   "12": "Dec"}

    data_array = date_time.split("/")
    print(date_time)
    print(data_array)
    year = data_array[-1]
    month = options_map.get(data_array[0])
    day = data_array[1]
    if len(day) == 1:
        day = "0" + day

    print("{}-{}-{}".format(year, month, day))

    d_eng(resourceId="com.jswjw.CharacterClient:id/add_btn", className="android.widget.Button").click()

    d_eng(resourceId="com.jswjw.CharacterClient:id/spinner", index=1, className="android.widget.Spinner").click()

    d_eng(resourceId="android:id/text1", index=1, className="android.widget.CheckedTextView").click()
    d_eng(resourceId="com.jswjw.CharacterClient:id/edittext", className="android.widget.TextView", index=1).click()

    d_eng(resourceId="android:id/numberpicker_input", text="Mar. Double tap to edit.", index=1).click()
    d_eng(resourceId="android:id/numberpicker_input", text="Mar. Editing.", index=1).set_text(month)

    # d(resourceId="android:id/numberpicker_input", text="10. Editing.", index=1).click()
    d_eng(resourceId="android:id/numberpicker_input", text="10. Editing.", index=1).set_text(day)

    # d(resourceId="android:id/numberpicker_input", text="2018. Editing.", index=1).click()
    d_eng(resourceId="android:id/numberpicker_input", text="2018. Editing.", index=1).set_text(year)

    d_eng(resourceId="android:id/button1", className="android.widget.Button", text="Set").click()

    d_eng(className="android.widget.LinearLayout", index=3).child(index=1).click()
    d_eng(className="android.widget.LinearLayout", index=3).child(index=1).set_text(ID)
    d_eng.press.back()

    d_eng(resourceId="com.jswjw.CharacterClient:id/edittext", text=". Double tap to edit.", index=1).click()
    d_eng(resourceId="com.jswjw.CharacterClient:id/edittext", text=". Editing.", index=1).set_text("tmp")
    d_eng.press.back()


    d_eng(resourceId="com.jswjw.CharacterClient:id/save_btn", text=u"保  存").click()


def input_name(name):
    d_chn(resourceId="com.jswjw.CharacterClient:id/title_txt", text="C T",index=0).long_click()
    d_chn(resourceId="com.jswjw.CharacterClient:id/item_value", text="tmp", index=2).long_click()
    #d_chn(resourceId="android:id/list", className="android.widget.ListView", index=2).child(index=1).click()
    d_chn(resourceId="com.jswjw.CharacterClient:id/edittext", text="tmp", index=1).set_text(name)
    d_chn(resourceId="com.jswjw.CharacterClient:id/save_btn", className="android.widget.Button").click()
    d_chn.press.back()
    d_chn.press.back()


#input_date("11/1/2016", "2469135")
#time.sleep(1)
#input_name(u"蒋秀美")


#CT_2016_11("11/1/2016", u"蒋秀美", "2469135")

def prepare_data():
    name_list = []
    id_list = []
    date_list = []

    with io.open("data/CT/2016-11/name.txt", "r", encoding='utf8') as f:
        for line in f.readlines():
            if line != "" and line != "\n":
                name_list.append(line)

    with io.open("data/CT/2016-11/ID.txt","r", encoding='utf8') as f:
        for line in f.readlines():
            if line != "" and line != "\n":
                id_list.append(line.strip())

    with io.open("data/CT/2016-11/date.txt","r", encoding='utf8') as f:
        for line in f.readlines():
            if line != "" and line != "\n":
                date_list.append(line.strip())

    total_id = random.sample(range(1, len(name_list[10:-10])), 550)
    total_id.sort()
    finished_id = []

    print(total_id)

    if not os.path.exists("total_id.pickle"):
        f = open("total_id.pickle", "wb")
        pickle.dump(total_id, f)
        f.close()

        f = open("finished_id.pickle", "wb")
        pickle.dump(finished_id, f)
        f.close()


def main():
    name_list = []
    id_list = []
    date_list = []

    #with io.open("data/CT/2016-11/name.txt", "r", encoding='utf8') as f:
    #    for line in f.readlines():
    #        if line != "" and line != "\n":
    #            name_list.append(line)

    lines = open("data/CT/2016-11/name.txt", encoding='utf-8').readlines()
    for line in lines:
        if line != "" and line != "\n":
            name_list.append(line.strip())

    with io.open("data/CT/2016-11/ID.txt","r", encoding='utf8') as f:
        for line in f.readlines():
            if line != "" and line != "\n":
                id_list.append(line.strip())

    with io.open("data/CT/2016-11/date.txt","r", encoding='utf8') as f:
        for line in f.readlines():
            if line != "" and line != "\n":
                date_list.append(line.strip())

    prepare_data()

    f = open("total_id.pickle", "rb")
    total_id = pickle.load(f)
    f.close()

    f_finised = open("finished_id.pickle", "rb")
    finished_id = pickle.load(f_finised)
    f_finised.close()

    print(len(total_id))
    print(len(finished_id))

    for id in total_id:
        time.sleep(1)
        if id in finished_id:
            continue

        print("Name {}".format(name_list[id]))
        print("Id {}".format(id_list[id]))
        print("Date {}".format(date_list[id]))

        # input_date("11/1/2016", "2469135")
        # time.sleep(1)
        # input_name(u"蒋秀美")
        try:
            input_date(date_list[id], id_list[id])
            time.sleep(1)
            input_name(name_list[id])
        except:
            return

        finished_id.append(id)

        f_finished = open("finished_id.pickle", "wb")
        pickle.dump(finished_id, f_finished)
        f_finished.close()


main()
