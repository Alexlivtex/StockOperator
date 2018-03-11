# -*- coding:utf-8 -*-

from uiautomator import Device
import random
import pickle

import time

import os
import io

ENG_DEVICE_ID = "3204928f588f1157"
CHN_DEVICE_ID = "2646acdf"

d_eng = Device(CHN_DEVICE_ID)
print(d_eng.info)

def prepare_data():
    name_list = []
    id_list = []
    date_list = []

    with io.open("data/CT/2017-05/name.txt", "r", encoding='utf8') as f:
        for line in f.readlines():
            if line != "" and line != "\n":
                name_list.append(line)

    with io.open("data/CT/2017-05/ID.txt","r", encoding='utf8') as f:
        for line in f.readlines():
            if line != "" and line != "\n":
                id_list.append(line.strip())

    with io.open("data/CT/2017-05/date.txt","r", encoding='utf8') as f:
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


def input_data(date_time, name, id):
    data_array = date_time.split("/")
    year = data_array[-1]

    month = data_array[0]

    day = data_array[1]
    if len(day) == 1:
        day = "0" + day

    print("{}-{}-{}".format(year, month, day))

    #Add
    d_eng(resourceId="com.jswjw.CharacterClient:id/add_btn", className="android.widget.Button").click()
    d_eng(resourceId="com.jswjw.CharacterClient:id/spinner", index=1, className="android.widget.Spinner").click()

    #Choose Cater
    d_eng(resourceId="android:id/text1", index=2, className="android.widget.CheckedTextView").click()
    d_eng(resourceId="com.jswjw.CharacterClient:id/edittext", className="android.widget.TextView", index=1).click()

    #Set time
    d_eng(text="2018").click()
    d_eng(className="android.widget.NumberPicker", index=0).child(resourceId="android:id/numberpicker_input", text="2018").set_text(year)

    d_eng(text="3").click()
    d_eng(className="android.widget.NumberPicker", index=1).child(resourceId="android:id/numberpicker_input", text="3").set_text(month)

    d_eng(text="11").click()
    d_eng(className="android.widget.NumberPicker", index=2).child(resourceId="android:id/numberpicker_input", text="11").set_text(day)

    d_eng(resourceId="android:id/button1").click()

    #Set ID
    d_eng(className="android.widget.LinearLayout", index=3).child(index=1).set_text(id)


    d_eng(text=u"病人姓名 : ").sibling(index=1).set_text(name)

    d_eng(resourceId="com.jswjw.CharacterClient:id/save_btn", text=u"保  存").click()

def main():
    name_list = []
    id_list = []
    date_list = []

    lines = open("data/CT/2017-05/name.txt", encoding='utf-8').readlines()
    for line in lines:
        if line != "" and line != "\n":
            name_list.append(line.strip())

    with io.open("data/CT/2017-05/ID.txt","r", encoding='utf8') as f:
        for line in f.readlines():
            if line != "" and line != "\n":
                id_list.append(line.strip())

    with io.open("data/CT/2017-05/date.txt","r", encoding='utf8') as f:
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
        #time.sleep(1)
        if id in finished_id:
            print("{} has already existed!".format(id))
            continue

        print("Name {}".format(name_list[id]))
        print("Id {}".format(id_list[id]))
        print("Date {}".format(date_list[id]))

        try:
            input_data(date_list[id], name_list[id], id_list[id])
        except:
            return

        finished_id.append(id)

        f_finished = open("finished_id.pickle", "wb")
        pickle.dump(finished_id, f_finished)
        f_finished.close()

    print("========================Finished Filling========================")
main()
