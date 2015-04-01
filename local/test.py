# -*- coding: utf-8 -*-
import os,re,sys,time

ifp = open(sys.argv[1],'r')
ofp1 = open(sys.argv[2],'w')
ofp2 = open(sys.argv[3],'w')
dict = {}
while True :
	line = ifp.readline()
	if not line :
		break
	line_list = re.split(' |\n',line)
	for x in range(1,6) :
		ofp1.write(line_list[0] + str(x) + " " + line_list[1] + " " + line_list[2] + str(x) + "\n")
		if dict.get(line_list[1]) == None :
			dict[line_list[1]] = line_list[1]
		if dict.get(line_list[2] + str(x)) == None :
			dict[line_list[2] + str(x)] = line_list[2] + str(x)
dict_list = dict.items()
dict_list.sort()

for i in range(0,len(dict_list)) :
	ofp2.write(dict_list[i][0] + "\n")
