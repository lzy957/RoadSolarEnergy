#test
#!/bin/bash
#author: Ziyu Liu

# get all filename in specified path

dress=_p
#current_path="$PWD"
current_path=/datadrive/urbanplayground/Streetview/View1
path=$1
#files=$(ls $path)
files=$(ls $current_path)
for filename in $files
do
 FilePath=$current_path/$filename
 if [ -d $FilePath ];then
	# echo "$FilePath"
	NFilePath=$FilePath/$filename
	if [ -d $NFilePath ];then
	 #      echo "$NFilePath"
 		 nfilename=$filename$dress
		find $NFilePath -name "*.jpg" -size -2k -exec rm {} \;
		export NFilePath	
	  	export nfilename
		export FilePath
	   	./demo_test.sh
        else	       
	 for i in $( seq 1 20 )
	 do
	 	 NFilePath=$FilePath/$filename${i}
	#	echo "$NFilePath"
		if [ -d $NFilePath ];then
			echo "$NFilePath"
			nfilename=$filename${i}$dress
			find $NFilePath -name "*.jpg" -size -2k -exec rm {} \;
			export NFilePath
			export nfilename
                	export FilePath
			./demo_test.sh
		fi
	 done
	fi
 fi
done
