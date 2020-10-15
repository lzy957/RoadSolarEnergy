# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 18:02:46 2019

@author: Ziyu Liu
"""

import cv2
import math
import numpy as np
from PIL import Image
from pylab import *
from PIL import ImageDraw
import os

#参考http://ju.outofmemory.cn/entry/34825
#批量参考https://blog.csdn.net/zong596568821xp/article/details/83586530


#filepath=r"./testimage"
cityname="Beijing"
rootpath="./"+cityname+"/SegPic"
for root, subdirs, files in os.walk(rootpath):
    for filepath in subdirs:
        writepathw = rootpath+"/"+filepath+"_pano"
        if not os.path.exists(writepathw):
            os.mkdir(writepathw)
        filepath =rootpath + "/" + filepath
        print(filepath)
        for filename in os.listdir(filepath):              #listdir的参数是文件夹的路径
            print ( filename)
            imagepath=filepath+"/"+filename             #此时的filename是文件夹中文件的名称
        #read original images
            try:
                origin_im = Image.open(imagepath)
                owidth = origin_im.size[0]
                realwidth = owidth/2
                oheight = origin_im.size[1]
                oR=int(oheight/2)
                R = 163
                #create new images
                #img = Image.new("1",(80,40),"white")#单色模式
                #img = Image.new("L",(80,40),200)#灰色模式
                img = Image.new("RGBA",(326,326),(0,0,0))#RGBA的真色模式
                draw = ImageDraw.Draw(img)
                img = img.convert("RGB")#jpg格式必须转换，单色和灰色不用
                width=img.size[0]
                height=img.size[1]
            except (OSError, NameError):
                print('OSError')
    
        #赋值
            for ox in range(owidth/2,owidth):
                for oy in range(oR):
                    o_r,o_g,o_b = origin_im.getpixel((ox,oy))
                    x =(oy/oR*163) * math.cos(math.pi/2-(realwidth/2-ox)/realwidth*2*math.pi)+R
                    y = -(oy/oR*163) * math.sin(math.pi/2-(realwidth/2-ox)/realwidth*2*math.pi)+R
                    x1=round(x)
                    y1=round(y)
                    x2=int(x)
                    y2=int(y)
                    r1,g1,b1 = img.getpixel((x1,y1))
                    r2,g2,b2 = img.getpixel((x2,y2))
                    if(x1==x2 and y1==y2):
                        if(r1==0 and g1==0 and b1==0):
                            img.putpixel((x1,y1),(o_r,o_g,o_b))
                        else:
                            img.putpixel((x1,y1),(int((o_r+r1)/2),int((o_g+g1)/2),int((o_b+b1)/2)))
                    else:
                        if(r1==0 and g1==0 and b1==0):
                            img.putpixel((x1,y1),(o_r,o_g,o_b))
                        else:
                            img.putpixel((x1,y1),(int((o_r+r1)/2),int((o_g+g1)/2),int((o_b+b1)/2)))
                        if(r2==0 and g2==0 and b2==0):
                            img.putpixel((x2,y2),(o_r,o_g,o_b))
                        else:
                            img.putpixel((x2,y2),(int((o_r+r2)/2),int((o_g+g2)/2),int((o_b+b2)/2)))
            #image转cv2
            imga = cv2.cvtColor(np.array(img),cv2.COLOR_RGB2BGR)
    
            # 中值滤波对滤除椒盐噪声
            median = cv2.medianBlur(imga, 3)
            cv2.imwrite(writepathw+"/"+filename, median)
