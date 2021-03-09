from urllib import request
import requests
import urllib.request
import os
import random
import math
import cv2
import numpy as np
import time
import csv
from skimage.morphology import disk
import skimage.filters.rank as sfr
from shutil import copyfile
import shutil

zoom = 18 #下载切片的zoom
trafficArray = np.zeros(32)
date = ["20190417","20190420"]
datestamp = ["2019-04-17","2019-04-20"]

def getTimeStamp(tssl):
	# 字符类型的时间
	#tss1 = '2019-04-06 05:00:00'
	# 转为时间数组
	timeArray = time.strptime(tssl, "%Y-%m-%d %H:%M:%S")
	#print (timeArray)     
	# timeArray可以调用tm_year等
	#print (timeArray.tm_year)   # 2019
	# 转为时间戳
	timeStamp = int(time.mktime(timeArray)-28800)
	#print (timeStamp) # 1381419600
	return timeStamp

def lonLat2tileCoord(lat_deg,lon_deg,zoom):
	#lonLat2MerCoord / worldCoordinate
	xMer = lon_deg * 20037508.34 / 180
	yMer = math.log(math.tan((90 + lat_deg) * math.pi /360)) / (math.pi /180)
	yMer = yMer * 20037508.34 / 180
	#print("Worldcoordinate:",xMer, yMer)
	#pixelCoordinate
	xPix = math.floor(xMer * math.pow(2,zoom - 18))
	yPix = math.floor(yMer * math.pow(2,zoom - 18))
	#print("pixelCoordinate:",xPix, yPix)
	#tileCoordinate
	xtile = math.floor(xPix /256)
	ytile = math.floor(yPix /256)
	#print("tileCoordinate:", xtile,ytile)
	xTpix = math.floor(xPix - xtile * 256)
	yTpix = math.floor(yPix - ytile * 256)
	return(xtile,ytile,xTpix,yTpix)   
    
def tileCoord2lonLat(xtile,ytile):
	lbx=xtile*256
	lby=ytile*256
	rtx=(xtile+1)*256
	rty=(ytile+1)*256
	wlbx=lbx/math.pow(2,zoom - 18)
	wlby=lby/math.pow(2,zoom - 18)
	wrtx=rtx/math.pow(2,zoom - 18)
	wrty=rty/math.pow(2,zoom - 18)
	lblon=wlbx*180/20037508.34
	lblat=math.arctan(math.exp((wlby*180/20037508.34)*math.pi/180)*360/math.pi)-90
	rtlon=wrtx*180/20037508.34
	rtlat=math.arctan(math.exp((wrty*180/20037508.34)*math.pi/180)*360/math.pi)-90
	return(lblon,lblat,rtlon,rtlat)

def getimg(ID, lat_deg, lon_deg):
    trafficArray = np.zeros(34)
    tilecoord=lonLat2tileCoord(float(lat_deg),float(lon_deg),zoom)
    counti = 0
    for j in range(0,2):
        for i in range(4,21):
            counti = counti + 1
            objtime = getTimeStamp(str(datestamp[j])+" "+str(i)+":00:00")
            path = r"./"+str(date[j])+str(i)
            originpath = path+"/{0}_{1}.jpg".format(tilecoord[0],tilecoord[1])
            if not os.path.exists(path):
                os.mkdir(path)
            pathgray = r"./"+str(date[j])+str(i)+"_gray"
            if not os.path.exists(pathgray):
                os.mkdir(pathgray)
            imgpath_save = pathgray+"/{0}_{1}.jpg".format(tilecoord[0],tilecoord[1])
            if not os.path.exists(imgpath_save):
                tilepath = "http://its.map.baidu.com:8002/traffic/TrafficTileService?level="+str(zoom)+"&x="+str(tilecoord[0])+"&y="+str(tilecoord[1])+"&time="+str(objtime)
                print(tilepath)
                try:
                    req=requests.get(tilepath,timeout=60)
		#print(req)
		#------------------------------edit------------------------
                    open(path+"/{0}_{1}.jpg".format(tilecoord[0],tilecoord[1]), 'wb').write(req.content)
                    print(ID,originpath,'success')
                    trafficArray[counti-1]=imgProcess(originpath, imgpath_save, tilecoord[2], tilecoord[3])
                    #print(trafficArray[counti-1])
                    os.remove(path+"/{0}_{1}.jpg".format(tilecoord[0],tilecoord[1]))
                except Exception as e:
                    trafficArray[counti-1]=-1
                    print(e,"exception\n")
            else:
                trafficArray[counti-1]=getTraffic(float(lat_deg),float(lon_deg),zoom,pathgray)
            print(trafficArray[counti-1])
            if trafficArray[0] == -1 or trafficArray[0] == 0:
                break 
        if trafficArray[0] == -1 or trafficArray[0] == 0:
                break
    return trafficArray
        
            

def getBaiduTile(time,path,pathgray):
    for x in range(lefttop[0]-1,rightbottom[0]):
    	for y in range(rightbottom[1]-1,lefttop[1]):
    		print(x,y)
    		tilepath = "http://its.map.baidu.com:8002/traffic/TrafficTileService?level="+str(zoom)+"&x="+str(x)+"&y="+str(y)+"&x="+str(time)
    		#tilepath="http://its.map.baidu.com:8002/traffic/TrafficTileService?level=12&x=791&y=295&time=1537268868766"
    		getimg(tilepath,path,pathgray,x,y,time)
    print("finish")

def file_name(root_path,picturetype):
    filename=[]
    for root,dirs,files in os.walk(root_path):
        for file in files:
            if os.path.splitext(file)[1]==picturetype:
                filename.append(os.path.join(root,file))
    return filename


def merge_picture(merge_path,num_of_cols,num_of_rows,xmin,ymax):
    filename=file_name(merge_path,".jpg")
    #print(filename[0])
    img_s=cv2.imread(filename[0])
    if img_s is None :
        img_s = cv2.imread("/home/user/PV/Traffic/Common.jpg")
    shape=img_s.shape
    #shape=cv2.imread(filename[0]).shape    #三通道的影像需把-1改成1
    cols=shape[1]
    rows=shape[0]
    channels=shape[2]
    print(cols,rows,channels)
    dst=np.zeros((rows*(num_of_rows+1),cols*(num_of_cols+1),channels),np.uint8)
    for i in range(len(filename)):
        img=cv2.imread(filename[i],1)
        if img is None:
            img = cv2.imread("/home/user/PV/Traffic/Common.jpg")
        imgname=filename[i].split("/")[-1]
        rows_th=ymax-int(imgname.split("_")[-1].split('.')[0])
        cols_th=int(imgname.split("_")[-2])-xmin
        if rows_th > num_of_rows:
            rows_th = rows_th - 1
        if cols_th > num_of_cols:
            cols_th = cols_th - 1
        if cols_th == -1:
            cols_th = cols_th + 1
        if rows_th == -1:
            rows_th = rows_th + 1
        print(rows_th,cols_th)
        roi=img[0:rows,0:cols,:]
        dst[rows_th*rows:(rows_th+1)*rows,cols_th*cols:(cols_th+1)*cols,:]=roi
    cv2.imwrite(merge_path+"merge.jpg",dst)

def getTraffic(lat_deg,lon_deg,zoom, Gpath):
    point=lonLat2tileCoord(lat_deg,lon_deg,zoom)
    img = cv2.imread( Gpath + "/{0}_{1}.jpg".format(point[0],point[1]),cv2.IMREAD_GRAYSCALE)
    #print(point[2],point[3])
    if img is not None:
        imgmax = sfr.maximum(img,disk(11))
        #blur = cv2.blur(img, (5,5))
        traffic_con=imgmax[point[2],point[3]]
    else:
        traffic_con=-1
    return (traffic_con)
    
def imgProcess(oimg_path,simg_path,xTpix,yTpix):
    img=cv2.imread(oimg_path,1)
    Grayimg=np.zeros((256,256),np.uint8)
    if img is not None:
        #Grayimg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        for j in range(255):
            for k in range(255):
                if img[j,k][0]==255 and img[j,k][1]==255 and img[j,k][2]==255:
                    Grayimg[j,k]=0
                elif img[j,k][1]>img[j,k][0] and img[j,k][1]>img[j,k][2]:
                    Grayimg[j,k]=10
                elif img[j,k][2]>img[j,k][0] and img[j,k][2]>img[j,k][1]:
                    if img[j,k][1]<100:
                        if img[j,k][2]>190:
                            Grayimg[j,k]=90
                        else:
                            Grayimg[j,k]=70
                    else:
                        Grayimg[j,k]=40
        #print(oimg_path,simg_path,xTpix,yTpix)
        imgmax = sfr.maximum(Grayimg,disk(11))
        #blur = cv2.blur(img, (5,5))
        traffic_con=imgmax[xTpix,yTpix]
        cv2.imwrite(simg_path,Grayimg)
    else:
        traffic_con=-1
    #print("/n imgprocess",traffic_con)
    return (traffic_con)
        


with open(r'./HEBAllPoints.csv', 'rb') as data:
    lines = data.readlines()
    with open(r'./hebtraffic04n.csv', 'w') as fileWriteObj:
        for i in range(1, len(lines)):
            lines[i]= lines[i].decode()
            longitude = lines[i].rstrip('\r').split(',')[3]
            latitude = lines[i].rstrip('\r').split(',')[4]
            #RID = lines[i].rstrip('\r').split(',')[5]
            ID = lines[i].rstrip('\r').split(',')[0]
            idd = lines[i].rstrip('\r').split(',')[1]
            rclass = lines[i].rstrip('\r').split(',')[2]
            latitude = latitude.strip('\t\r\n')
            #RID = RID.strip('\t\r\n')
            print (ID, idd, rclass, longitude, latitude)
            res = getimg(ID,latitude, longitude)
            writer = csv.writer(fileWriteObj, lineterminator='\n')
            writer.writerow([ID, idd, rclass, longitude, latitude, res])
        print("finish"+str(i))

