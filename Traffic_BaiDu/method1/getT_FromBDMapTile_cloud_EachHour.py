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

def getTimeStamp(tssl):
	# 字符类型的时间
	#tss1 = '2019-04-06 05:00:00'
	# 转为时间数组
	timeArray = time.strptime(tssl, "%Y-%m-%d %H:%M:%S")
	#print (timeArray)     
	# timeArray可以调用tm_year等
	#print (timeArray.tm_year)   # 2019
	# 转为时间戳
	timeStamp = int(time.mktime(timeArray))
	#print (timeStamp) # 1381419600
	return timeStamp

#def deg2num(lat_deg,lon_deg,zoom):
#	lat_rad = math.radians(lat_deg)
#	n = 2.0 ** zoom
#	xtile = int((lon_deg+180.0)/360.0*n)
#	ytile = int((1.0 - math.log(math.tan(lat_rad)+(1/math.cos(lat_rad)))/math.pi)/2.0*n)
#	return ( xtile, ytile)

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

def getimg(Tpath, Spath, Gpath, x, y, Timea):
        for i in range(10):
                try:
		#f = open(Spath,'wb')
		#req = urbllib.request.Request(Tpath)
                        req=requests.get(Tpath)
		#print(req)
		#------------------------------edit------------------------
                        open(Spath+"/{0}_{1}.jpg".format(x,y), 'wb').write(req.content)
		#pic = urllib.request.urlopen(req, timeout=60)
		#f.write(pic.read())
		#f.close()
                        print(str(x)+'_'+str(y)+'success')
                        imgProcess( Spath, Gpath)
                        os.remove(Spath+"/{0}_{1}.jpg".format(x,y))
                except Exception as e:
                        if i>=9:
                                open("BDTraffic.txt", 'a').writelines(e)
                                print(str(x)+'_'+str(y)+'Failed, ReTry!')
                                do_some_log()
                        else:
                                time.sleep(0.5)
                else:
                        time.sleep(0.1)
                        break
		#getimg(Tpath, Spath, x, y)

def getBaiduTile(time,path,pathgray):
    for x in range(lefttop[0]-1,rightbottom[0]):
    	for y in range(rightbottom[1]-1,lefttop[1]):
    		print(x,y)
    		tilepath = "http://its.map.baidu.com:8002/traffic/TrafficTileService?level="+str(zoom)+"&x="+str(x)+"&y="+str(y)+"&time="+str(time)
    		#tilepath="http://its.map.baidu.com:8002/traffic/TrafficTileService?level=12&x=791&y=295&time=1537268868766"
    		#getimg(tilepath,os.path.join(path,str(x)+"_"+str(y)+".png"),x,y)
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
    img = cv2.imread( Gpath + "{0}_{1}.jpg".format(point[0],point[1]),cv2.IMREAD_GRAYSCALE)
    #print(point[2],point[3])
    if img is not None:
        imgmax = sfr.maximum(img,disk(11))
        #blur = cv2.blur(img, (5,5))
        traffic_con=imgmax[point[2],point[3]]
    else:
        traffic_con=-1
    return (traffic_con)
    
def imgProcess(oimg_path,simg_path):
    filename=file_name(oimg_path,".jpg")
    for i in range(len(filename)):
        img=cv2.imread(filename[i],1)
        Grayimg=np.zeros((256,256,1),np.uint8)
        if img is not None:
            #Grayimg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            for j in range(255):
                for k in range(255):
                    if img[j,k][0]==255 and img[j,k][1]==255 and img[j,k][2]==255:
                        Grayimg[j,k]=0
                    elif img[j,k][1]>img[j,k][0] and img[j,k][1]>img[j,k][2]:
                        Grayimg[j,k]=30
                    elif img[j,k][2]>img[j,k][0] and img[j,k][2]>img[j,k][1]:
                        if img[j,k][1]<100:
                            if img[j,k][2]>190:
                                Grayimg[j,k]=90
                            else:
                                Grayimg[j,k]=70
                        else:
                            Grayimg[j,k]=50
            print(filename[i].split('/')[-1])
            cv2.imwrite(str(simg_path)+str(filename[i].split('/')[-1]),Grayimg)
        else:
            copyfile(filename[i], str(simg_path)+str(filename[i].split('/')[-1]))
        

zoom = 18 #下载切片的zoom
lefttop = lonLat2tileCoord(41.05832,115.4191,zoom)
rightbottom = lonLat2tileCoord(39.44818,117.4983,zoom)

num_of_cols = rightbottom[0]-lefttop[0]
num_of_rows = lefttop[1] - rightbottom[1]

print(str(lefttop[0]))
print(str(rightbottom[0]))
print(str(lefttop[1]))
print(str(rightbottom[1]))
print("totally"+str(rightbottom[0]-lefttop[0]))
print("totally"+str(lefttop[1] - rightbottom[1]))


date = ["20190417","20190420"]
datestamp = ["2019-04-17","2019-04-20"]
for j in range(0,2):
    for i in range(5,11):
        objtime = getTimeStamp(str(datestamp[j])+" "+str(i)+":00:00")
        path = r"/home/user/PV/Traffic/Beijing/"+str(date[j])+str(i)+"/"
        if not os.path.exists(path):
            os.mkdir(path)
        pathgray = r"/home/user/PV/Traffic/Beijing/"+str(date[j])+str(i)+"_gray/"
        if not os.path.exists(pathgray):
            os.mkdir(pathgray)
        getBaiduTile(objtime,path,pathgray)
        ##merge_picture(path,num_of_cols,num_of_rows,lefttop[0],lefttop[1])
        print("finish"+str(i))
        with open(r'/home/user/PV/Traffic/Beijing/Points/beijing_chouxi_150.csv', 'rb') as data:
            lines = data.readlines()
            with open(r'/home/user/PV/Traffic/Beijing/'+str(date[j])+str(i)+'.csv', 'w') as fileWriteObj:
                for i in range(1, len(lines)):
                    lines[i]= lines[i].decode()
                    longitude = lines[i].rstrip('\r').split(',')[3]
                    latitude = lines[i].rstrip('\r').split(',')[4]
                    RID = lines[i].rstrip('\r').split(',')[5]
                    ID = lines[i].rstrip('\r').split(',')[0]
                    idd = lines[i].rstrip('\r').split(',')[1]
                    rclass = lines[i].rstrip('\r').split(',')[2]
                    RID = RID.strip('\t\r\n')
                    print (ID, idd, rclass, longitude, latitude)
                    traffic = getTraffic(float(latitude),float(longitude),18,pathgray)
                    writer = csv.writer(fileWriteObj, lineterminator='\n')
                    writer.writerow([ID, RID, idd, rclass, longitude, latitude, traffic])
            shutil.rmtree(pathgray)

#os.remove('/home/user/PV/Traffic/Beijing/Workday_6_gray')

#imgProcess("/home/user/PV/Traffic/Beijing/Workday_6/","/home/user/PV/Traffic/Beijing/Workday_6_gray/")



