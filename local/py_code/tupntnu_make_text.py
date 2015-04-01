# -*- coding: utf-8 -*-
import os,re,sys
from optparse import OptionParser

def Trans2U(str) :
	length = 4 - len(str)
	key = "U"
	for i in range(0,length) :
		key += '0'
	key += str
	return key

if len(sys.argv) != 3 and len(sys.argv) != 5 and len(sys.argv) != 7 :
	print "Usage: " + sys.argv[0] + " [options] <ms-info> <output-txt>"
	print "e.g.: " + sys.argv[0] + " -l 2 -p True /mnt/corpus/TUP_NTNU/MS.info data/MS_L1_T/text "
	print "options: "
	print "\t-l\t1 : native language learner, 2 : other language learner (default = None) . "
	print "\t-p\tPronunciation True or False (default = None) . "
	print "			"
	exit()

# Main

ll = "None"
p = "NONE"

parser = OptionParser()
parser.add_option("-l", dest="ll")
parser.add_option("-p", dest="p")
(options, args) = parser.parse_args()
ll = options.ll
ll = str(ll)
p = options.p
p = str(p).upper()

ifp = open(sys.argv[len(sys.argv)-2],'r') # MS.info
ofp = open(sys.argv[len(sys.argv)-1],'w') # text
ms_dict = {}

line = ifp.readline()
field = ['\xe8\xa9\x95\xe9\x9f\xb3\xe4\xba\xba', 'Student_ID', 'Syllable', 'OriInitial', 'OriFinal OriTone MsId', 'ActInitial', 'ActFinal', 'ActTone', 'National', 'Gender', 'InitCorrect', 'FinalCorrect', 'ToneCorrect', 'KInit', 'KFinal', 'KTone', 'KTonalFinal', '']
line_list = re.split('\t|\n',line)
if line_list != field :
	print "[Error] data format error!"
	exit()

while True :
	line = ifp.readline()
	if not line :
		break
	line_list = re.split('\t|\n',line)
	
	key = Trans2U(line_list[1]) + "_" + line_list[6]
	if ms_dict.get(key) == None :
		# [initial,final+tone,評音人,國籍,OX,OX,OX]
		ms_dict[key] = [line_list[3],line_list[4]+line_list[5],line_list[0],line_list[10],line_list[12],line_list[13],line_list[14]]
	else : # 優先順序為 1.Admin 2.劉珮君 3.熊玉雯
		if ms_dict[key][2] != "Admin" and line_list[0] == "Admin" :
			ms_dict[key] = [line_list[3],line_list[4]+line_list[5],line_list[0],line_list[10],line_list[12],line_list[13],line_list[14]]
		elif ms_dict[key][2] != "劉姵君" and (line_list[0] == "Admin" or line_list[0] == "劉姵君") :
			ms_dict[key] = [line_list[3],line_list[4]+line_list[5],line_list[0],line_list[10],line_list[12],line_list[13],line_list[14]]
		elif ms_dict[key][2] != "熊玉雯" and (line_list[0] == "Admin" or line_list[0] == "劉姵君" or line_list[0] == "熊玉雯") :
			ms_dict[key] = [line_list[3],line_list[4]+line_list[5],line_list[0],line_list[10],line_list[12],line_list[13],line_list[14]]
ifp.close()

work_flag = 0
count=0
ms_dict_list = ms_dict.items()
ms_dict_list.sort()
for i in range(0,len(ms_dict_list)) :
	if (p == "TRUE" and ms_dict_list[i][1][4] == 'O' and ms_dict_list[i][1][5] == 'O' and ms_dict_list[i][1][6] == 'O') or p == "NONE" :
		if (ll == "1" and ms_dict_list[i][1][3] == "台灣") or ll == "None" :
			work_flag = 1
		elif (ll == "2" and ms_dict_list[i][1][3] != "台灣") or ll == "None" :
			work_flag = 1
		else :
			work_flag = 0
	elif (p == "FALSE" and (ms_dict_list[i][1][4] == 'X' or ms_dict_list[i][1][5] == 'X' or ms_dict_list[i][1][6] == 'X')) or p == "NONE" :
		if (ll == "1" and ms_dict_list[i][1][3] == "台灣") or ll == "None" :
			work_flag = 1
		elif (ll == "2" and ms_dict_list[i][1][3] != "台灣") or ll == "None" :
			work_flag = 1
		else :
			work_flag = 0
	else :
		work_flag = 0
		
	if work_flag == 1 :
		if ms_dict_list[i][1][0] == 'sic' :
			ofp.write(ms_dict_list[i][0] + " " + ms_dict_list[i][1][1] + "\n")
		else :
			ofp.write(ms_dict_list[i][0] + " " + ms_dict_list[i][1][0] + ms_dict_list[i][1][1] + "\n")
		count+=1
ofp.close()
		
print "Total " + str(count) + " utterances."
