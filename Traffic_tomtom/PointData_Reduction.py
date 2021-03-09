import csv

ridtemp=0
count=0
with open('shenzhen_chouxi_150.csv', 'w') as f:
	writer = csv.writer(f)
	#for filenum in range(1,30):
		#filepath='C:/Users/Administrator/Desktop/tomtom/point/p'+str(filenum)+'.csv'
	filepath='/Users/lzy/Documents/SZAllPoints.csv'
	with open(filepath, 'r') as data:
		#lines = data.readlines()
		reader=csv.reader(data)
		head_row = next(reader)
		#print (list(reader)[0])
		for row in reader:
		# Get coordinate
			#print(reader.line_num, row)
			#longitude=row[4]
			#latitude=row[3]
			ID = row[0]
			#row[0]=int(ID)+filenum*100000
			row[0]=int(ID)
			roadid=row[1]
			print(reader.line_num, row)
			#print ([longitude,latitude,ID,roadid])
			if roadid==ridtemp:
				count+=1
				if count%3==1:
					writer.writerow(row)
			else:
				count=1
				ridtemp=roadid
				writer.writerow(row)
