"""
Input: 
Requires a "InvChain.sp" as input, to avoid overwrite other .sp file in
the same directory, this function can also feed in argument to indicate the
file name of test .sp file. 

Also, don't forget to put the library file
"cmoslibrary.lib" under the same directory.


Output: 
A print out of list tphl_inv, with the Makefile, those result will be
put into "data.txt" 

Main tasks of this file:
1. Run hspice using InvChain.sp as an input deck
2. Read the resulting tphl_inv from output
3. Change the InvChain.sp deck to look for a better value of tphl_inv

In this project, I try to write a file called "InvChainTest.sp" with the maximum case of Inverter at beginning, and I stored the content of target spice file
"InvChain.sp" in a list called "init_list".

Each time I want to run a simulation with different parameters, I change the
corresponding context in "init_list" and write to "InvChainTest.sp", in this
case I won't have to always read file and it should make this script file runs
faster.

Conclusion:
Finally a result is printed and I use a simple Python file(Proj4_plot.py) to plot for result.
From my 42 result, the best delay time(shortest) is at the condition: Inverter
numbers = 5, fan = 4, which tphl_inv = 5.7877340000000001e-10

The first graph shows the best result falls at fan = 4
The second graph shows the best result is obtained from Inverter number
= 5

"""

## Run hspice InvChain.sp
from subprocess import call
import sys
import re

out_filename = "result.txt"
tphl_inv_list = []
fan_list = []
inv_num_list = []

if len(sys.argv) > 1: 
    sp_filename = sys.argv[1]
else:   
    sp_filename = "InvChainTest.sp"

sp_init_filename = "InvChain.sp"
max_inv_num = 11
max_fan_num = 7

##with open(sp_filename,"r+") as fs:
with open(sp_init_filename,"r+") as fs:
	init_list = fs.readlines()
fs.close()

## For convenience, I first scan through the initial InvChain.sp and try to get the infomations about
## The number of Inv, also the starting line of Xinv, and the position of the node declaration
## The line of the .measure, also the position of the Xinv#.z
Xinv_start_index = 0
Xinv_cnt = 0
Xinv_end_pos = 0
measure_index = 0
measure_pos = 0

for i,ival in enumerate(init_list):
    	if re.search(r'^Xinv(\w+)',ival):
    	    	if not Xinv_start_index: ## only do it first time
    	    	    	Xinv_start_index = i
    	    	    	x = re.compile(r'\s[a-z]\s[a-z]\s')
    	    	    	y = x.finditer(ival)
    	    	    	for j in y:
    	    	        	Xinv_end_pos = j.start()+3
    	    	Xinv_cnt += 1
    	if re.search(r'^[.]measure',ival):
    	    	measure_index = i
    	    	x = re.compile(r'Xinv\d[.]z')
    	    	y = x.finditer(ival)
    	    	for j in y:
    	        	measure_pos = j.start()+4

##print("inv index:",Xinv_start_index)
##print("inv cnt:",Xinv_cnt)
##print("inv end pos:",Xinv_end_pos)
##print("mea index:",measure_index)
##print("mea pos:",measure_pos)


## Generate a full case (with 11 inverters)
tmp = ""
for i in range(max_inv_num):
    	if i == Xinv_cnt-1:
    	    	tmp = init_list[Xinv_start_index+i][:Xinv_end_pos]+chr(ord("a")+i+1)+init_list[Xinv_start_index+i][Xinv_end_pos+1:]
    	    	init_list[Xinv_start_index+i] = tmp
    	elif i > Xinv_cnt-1:
    	    	if i < 10:
    	    	    	tmp = tmp[:Xinv_end_pos-2]+chr(ord("a")+i)+" "+chr(ord("a")+i+1)+tmp[Xinv_end_pos+1:-1]+"*fan"+"\n"
    	    	    	tmp = tmp[:4]+str(i+1)+tmp[5:]
    	    	else:
    	    	    	tmp = tmp[:Xinv_end_pos-1]+chr(ord("a")+i)+" "+chr(ord("a")+i+1)+tmp[Xinv_end_pos+2:-1]+"*fan"+"\n"
    	    	    	tmp = tmp[:4]+str(i+1)+tmp[6:]
    	    	if i == max_inv_num-1:
    	    	    	tmp = tmp[:Xinv_end_pos+1]+"z"+tmp[Xinv_end_pos+2:]
    	    	init_list.insert(Xinv_start_index+i,tmp)

init_list[measure_index+(max_inv_num-Xinv_cnt)] = init_list[measure_index+(max_inv_num-Xinv_cnt)][:measure_pos]+str(max_inv_num)+init_list[measure_index+(max_inv_num-Xinv_cnt)][measure_pos+1:]

with open(sp_filename,"w+") as fs:
	fs.writelines(init_list)
fs.close()

for inv_num in range(max_inv_num,-1,-2):
	## 3 actions to do
	## 	a. comment out redundant XInv
	## 	b. change the last node to z
	##	c. change # of the XInv#.z in the line of .measure
	if inv_num != max_inv_num:
		## a.
		for i in range(inv_num,inv_num+2):
			init_list[Xinv_start_index+i] = "**"+init_list[Xinv_start_index+i]
		
		## b.
		tmp = init_list[Xinv_start_index+inv_num-1]
		if inv_num > 9:
			init_list[Xinv_start_index+inv_num-1] = tmp[:Xinv_end_pos+1]+"z"+tmp[Xinv_end_pos+2:]
		else:
			init_list[Xinv_start_index+inv_num-1] = tmp[:Xinv_end_pos]+"z"+tmp[Xinv_end_pos+1:]
		
		## c.
		tmp = init_list[measure_index+(max_inv_num-Xinv_cnt)]
		init_list[measure_index+(max_inv_num-Xinv_cnt)] = tmp.replace("Xinv"+str(inv_num+2),"Xinv"+str(inv_num))

	for fan in range(1,max_fan_num+1):
		## 3 actions to do
		## 	a. change fan
		## 	b. write back init_list
		## 	c. run hspice with system call, into the out_filename
		##	d. extract tphl_inv info from out_filename

		## a.
        	init_list[10] = ".param fan = "+str(fan)+"\n"

		## b.
        	with open(sp_filename,"w") as fs:
        	    fs.writelines(init_list)

        	fs.close()
        	
		## c.
        	call(["hspice", sp_filename, ">", out_filename])

		## d.
        	with open(out_filename,"r") as fs:
        	    spice_list = fs.readlines()

		found = []
        	for i in spice_list:
        	    if re.search(r'tphl_inv',i):
        	        found = re.findall(r'(\w+)\s*=\s*(\d+[.]*\d*)(\w)',i)
        	        print(found)
			if found[0][2] == "p":
        	        	tphl_inv_list.append(float(found[0][1])*1e-12)
			elif found[0][2] == "u":
        	        	tphl_inv_list.append(float(found[0][1])*1e-6)
			else:## Default case is "n"
        	        	tphl_inv_list.append(float(found[0][1])*1e-9)
        	        fan_list.append(fan)
        	        inv_num_list.append(inv_num)

        	if not found: 
			print("Not Found!!!")
			break

print("RESULT")
min_result = []
for i in range(len(tphl_inv_list)/max_fan_num):
	print(tphl_inv_list[i*max_fan_num:i*max_fan_num+max_fan_num])
	min_result.append(min(tphl_inv_list[i*max_fan_num:i*max_fan_num+max_fan_num]))

print(fan_list)
print(inv_num_list)

x = tphl_inv_list.index(min(tphl_inv_list))
ideal_inv_num = max_inv_num - (x // max_fan_num)*2
ideal_fan = x % max_fan_num + 1
print(x,ideal_inv_num,ideal_fan)

