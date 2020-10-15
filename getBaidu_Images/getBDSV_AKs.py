# coding:utf-8      
# version:python3.6
# author:Ziyu Liu
# collect street view data from BaiduMap
# Guidance:http://lbsyun.baidu.com/index.php?title=viewstatic


import requests
import os
import time
import json
import sys
angles = [0,90,180,270]
pitchs = [45,90]

#BaiduAK.txt is the file of Your Baidu AKs
with open(r'./BaiduAK.txt', 'r') as apis:
    apilines = apis.readlines()
    #print("read")

# Baidu API request
class BaiduAPI(object):
    def __init__(self):
        # Your Baidu AK
        self.ak = apilines[0].strip('\t\r\n')
        self.keycount = 1
        #print("set")

    # Each search request
    def search_photo(self, longitude, latitude,ID):
        filesize = 0
        data = {
            "ak": self.ak,
            "height": "360",
            "width": "1024",
            "location": "{0},{1}".format(latitude,longitude),
            "fov": "360",
            "pitch": "0",
            "heading": "0",
            "coordtype":"wgs84ll",
        }
        try:
            # Download pictures
            r = requests.get("http://api.map.baidu.com/panorama/v2?", params=data)
            r.encoding='utf-8'
            print(self.ak)
            savepath="./{0}_{1}_{2}.jpg".format(ID,longitude,latitude)
            open(savepath, 'wb').write(r.content)
            filesize=os.stat(savepath).st_size
            # 301 Permanent quota exceeds limit, rest
            if filesize > 200:
                return filesize
            else:
                data = r.json()
                print(data)
                status = data["status"] 
                print (status)
                # 301 Permanent quota exceeds limit, restrict access
                # 302 Day quota exceeded, restrict access
                if status == "301" or status == "302" or status == "201":
                    print("301/2")
                    os.remove(savepath)
                    print ("-----------------keychange----------------------\n")
                    print (self.keycount,self.ak,ID)
                    #time.sleep(3)
                    if int(self.keycount) < len(apilines):
                        remainnum = int(len(apilines))-int(self.keycount)
                        print ("We still have %d AKs"%remainnum)
                        #self.keycount = int(self.keycount) + 1
                        self.ak = apilines[self.keycount-1].strip('\t\r\n')
                        del apilines[0]
                        print ("current key count is %s, no. %d"%(self.ak,self.keycount))
                        print ("--------Request Again---------")
                        filesize = self.search_photo(longitude,latitude,ID)
                    else:
                        print("ALL AKs HAVE DONE and LAST ID is %s"%ID)
                        filesize = 0
                        sys.exit(1)
                # 401 The current concurrency has exceeded the agreed concurrency quota, restrict access
                elif status == "401" :
                    print('401')
                    os.remove(savepath)
                    print ("--------request failed Try Again---------")
                    filesize=self.search_photo(longitude,latitude,ID)
                else:
                    os.remove(savepath)
                    filesize = 0
        except Exception as e:
            # open("BSV.txt", 'a').writelines(e)
            print(e)
        print ("--------filesize  %s-------------"%filesize)
        return filesize

            
if __name__ == '__main__':
	# Read data from csv
	with open(r'./point_example.csv', 'r') as data:
		lines = data.readlines()
		for i in range(19950,len(lines)):
			# Get coordinates
			latitude = lines[i].split(',')[3]
			longitude = lines[i].split(',')[4]
			ID = lines[i].split(',')[0]
			longitude=longitude.strip('\t\r\n')
			# Get pictures
			baidu = BaiduAPI()
			print(longitude, latitude,ID)
			#time.sleep(2)
			baidu.search_photo(longitude,latitude,ID)
