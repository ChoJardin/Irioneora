# mapper 


# https://github.com/vizkids/Map-Reduce-powered-kNN-algorithm/blob/master/mapper.py
#!/usr/bin/env python
import sys
import math
inputval = [sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]]
for lines in sys.stdin:
	avg = 0.0
	lines = lines.strip()
	features = lines.split(',')
	for i in range(len(features)-1):
		if features[i]!='':
			avg += (float(features[i]) - float(inputval[i]))**2
			dist = math.sqrt(avg)
	features.append(str(dist))
	print ','.join(features)


# reducer
#!/usr/bin/env python
import sys
from operator import itemgetter
distances=[]
estimateval = 0.0
k=3
#k=int(sys.argv[1])

for lines in sys.stdin:
	lines=lines.strip()
	elements = lines.split(',')
	distances.append(elements)
distances = sorted(distances,key=itemgetter(-1))

for i in range(k):
	try:
		estimateval += float(distances[i][-2])
	except ValueError:
		continue
	
print estimateval


# wrapper

#!/usr/bin/env python
from random import randrange
from subprocess import call,check_output
import os,time

start_time = time.time()
FNULL = open(os.devnull, 'w')
OUTPUT_DIR = '/locals/knn/output'


lps = raw_input("What processor speed of your laptop?			:	")
lrm = raw_input("What is the RAM memory of your laptop?			:	")
lhd = raw_input("What is the Hard Disk Capacity of your laptop?		:	")
lss = raw_input("What is the screen size of your laptop?		:	")
nn = raw_input("Enter the number of nearest neighbours to compare	:	")

status = call("hdfs dfs -test -d "+OUTPUT_DIR,stdout=FNULL,stderr=FNULL,shell=True)
if status == 0:call("hdfs dfs -rm -r "+OUTPUT_DIR,stdout=FNULL,stderr=FNULL,shell=True)
command_string = "hadoop  jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar \
-input /locals/knn/input \
-output /locals/knn/output \
-mapper 'mapper.py "+str(lps)+" "+str(lrm)+" "+str(lhd)+" "+str(lss)+" "+"' \
-reducer 'reducer.py "+str(nn)+"' \
-file ~/projects/bigdata/mapreduce/knn/mapper.py \
-file ~/projects/bigdata/mapreduce/knn/reducer.py"

return_code = call(command_string,stdout=FNULL,stderr=FNULL,shell=True)
if return_code == 0: 
	estval = check_output("hdfs dfs -cat "+OUTPUT_DIR+"/*",shell=True)
	print "\n"
	print "	===	RESULTS		==="	
	print "\n"
	print "Estimated price for your configuration : $"+str(estval)
	print "Time Taken	:	%s seconds " % (time.time() - start_time)
    
