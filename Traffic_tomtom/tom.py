# coding:utf-8
# version:python2.7
# author:Yuhao Kang
# collect street view data from BaiduMap

import requests
import sys
import time
import datetime
import sched
import csv
import json
from threading import Timer
import urllib
import http.client
import urllib

year=2020
date=3
month=4
startTime0 = datetime.datetime(year, month, date, 4, 00, 0)
startTime1 = datetime.datetime(year, month, date, 5, 00, 0)
startTime2 = datetime.datetime(year, month, date, 6, 00, 0)
startTime3 = datetime.datetime(year, month, date, 7, 00, 0)
startTime4 = datetime.datetime(year, month, date, 8, 00, 0)
startTime5 = datetime.datetime(year, month, date, 9, 00, 0)
startTime6 = datetime.datetime(year, month, date, 10, 00, 0)
startTime7 = datetime.datetime(year, month, date, 11, 00, 0)
startTime8 = datetime.datetime(year, month, date, 12, 00, 0)
startTime9 = datetime.datetime(year, month, date, 13, 00, 0)
startTime10 = datetime.datetime(year, month, date, 14, 00, 0)
startTime11 = datetime.datetime(year, month, date, 15, 00, 0)
startTime12 = datetime.datetime(year, month, date, 16, 00, 0)
startTime13 = datetime.datetime(year, month, date, 17, 00, 0)
startTime14 = datetime.datetime(year, month, date, 18, 00, 0)
startTime15 = datetime.datetime(year, month, date, 19, 00, 0)
startTime16 = datetime.datetime(year, month, date, 20, 00, 0)
timelist=[startTime0,startTime1,startTime2,startTime3,startTime4,startTime5,startTime6,startTime7,startTime8,startTime9,startTime10,startTime11,startTime12,startTime13,startTime14,startTime15,startTime16]
#timelist=[startTime0,startTime1,startTime2,startTime3,startTime4,startTime13,startTime14,startTime15]

# 初始化sched模块的scheduler类
# 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。
schedule = sched.scheduler(time.time, time.sleep)

with open(r'C:/Users/Administrator/Desktop/cities/Tomtom_map_key.txt', 'r') as apis:
    apilines = apis.readlines()
    # print len(apilines)

# global variable
currentS = -1
freeFS = -1
class BaiduAPI(object):
    def __init__(self):
        # Your google api key

        self.api_key = apilines[0].strip('\t\r\n')
        self.keycount = 1
        # self.api_key = "3YyusDZnb4VBuefTx5wTQHuFWnYSx7hm"

    def search_photo(self, longitude, latitude,ID,timecount):
       	params = {
            "openLr": "true",
            "point": "{0},{1}".format(latitude,longitude),
            "key": self.api_key,
        }
        try:
            global currentS, freeFS
            # proxies = {'https': 'https://web-proxy.oa.com:8080',
            #            'http': 'http://web-proxy.oa.com:8080'}

            # r = requests.get("https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/18/json?", params, proxies=proxies)
            r = requests.get("https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/18/json?", params)
            #print (r)
            if r.status_code == 200:
                js = r.json()
                # print js
                currentS = js["flowSegmentData"]["currentSpeed"]
                freeFS = js["flowSegmentData"]["freeFlowSpeed"]
                #print (currentS, freeFS)
            elif r.status_code == 400:
                currentS = 0
                freeFS = 0
                #print currentS, freeFS
            elif r.status_code == 403:
                print ("!!!!!!!!!!!!" + "key change")
                print (self.keycount)
                #print len(apilines)
                if int(self.keycount) < len(apilines):
                    self.keycount = int(self.keycount) + 1
                    self.api_key = apilines[self.keycount-1].strip('\t\r\n')
                print ("current key count is ")
                print (self.keycount)

                print ("request the fail request again~~~~~~")
                res = self.search_photo(longitude, latitude, ID, timecount)
                currentS = res[0]
                freeFS = res[1]
                print ("^^^^^^^^^^^")

            return (currentS, freeFS)

        except Exception as e:
            info = sys.exc_info()
            print (e)    #打印捕获的异常对象
            print (info) #打印异常的完整数据

if __name__ == '__main__':

    baidu = BaiduAPI()

    with open(r'C:/Users/Administrator/Desktop/cities/beijing/TrafficP/beijing_tom_1.csv', 'r') as data:
        lines = data.readlines()
        print (datetime.datetime.now())
        print ("success")

        for j in range(0, len(timelist)):
            print ("111")

            while datetime.datetime.now() < timelist[j]:
                print (datetime.datetime.now())
                time.sleep(60)
                print ("222")

            timecount = 0
            for k in range(0, len(timelist)):
                if datetime.datetime.now() > timelist[k]:
                    print (datetime.datetime.now())
                    print (timelist[k])
                    timecount = timecount + 1
                    print (timecount)
            with open("./Workday/beijingwork1_" + str(timecount) + ".csv", 'w') as fileWriteObj:
                for i in range(1, len(lines)):
                    longitude = lines[i].rstrip('\r').split(',')[4]
                    latitude = lines[i].rstrip('\r').split(',')[3]
                    ID = lines[i].rstrip('\r').split(',')[0]
                    idd = lines[i].rstrip('\r').split(',')[1]
                    rclass = lines[i].rstrip('\r').split(',')[2]
                    longitude = longitude.strip('\t\r\n')
                    print (ID, idd, rclass, longitude, latitude)

                    result = baidu.search_photo(longitude, latitude, ID, timecount)

                    writer = csv.writer(fileWriteObj, lineterminator='\n')

                    writer.writerow([ID, idd, rclass, longitude, latitude, result[0], result[1]])

                if j == 17:
                    break
                while datetime.datetime.now() < timelist[j]:
                    print (datetime.datetime.now())
                    print (timelist[j])
                    time.sleep(20)





        # for j in range(0,len(timelist)):
        #     timecount = 0
        #     for k in range(0, len(timelist)):
        #         if datetime.datetime.now() > timelist[k]:
        #             print datetime.datetime.now()
        #             print timelist[k]
        #             timecount = timecount + 1
        #             print timecount
        #     with open("speed1_" + str(timecount) + ".csv", 'w') as fileWriteObj:
        #         for i in range(1, len(lines)):
        #             longitude = lines[i].rstrip('\r').split(',')[4]
        #             latitude = lines[i].rstrip('\r').split(',')[3]
        #             ID = lines[i].rstrip('\r').split(',')[0]
        #             idd = lines[i].rstrip('\r').split(',')[1]
        #             rclass = lines[i].rstrip('\r').split(',')[2]
        #             longitude = longitude.strip('\t\r\n')
        #             print ID, idd, rclass, longitude, latitude
        #
        #             result = baidu.search_photo(longitude, latitude, ID, timecount)
        #
        #             writer = csv.writer(fileWriteObj, lineterminator='\n')
        #
        #             writer.writerow([ID, idd, rclass, longitude, latitude, result[0], result[1]])
        #
        #         if j == 13:
        #             break
        #         while datetime.datetime.now() < timelist[j]:
        #             print datetime.datetime.now()
        #             print timelist[j]
        #             time.sleep(20)
