# -*- coding: utf-8 -*-
import os,re,sys

def edit(str1, str2):  
      
    matrix = [[i+j for j in range(len(str2) + 1)] for i in range(len(str1) + 1)]  
  
  
    for i in xrange(1,len(str1)+1):  
        for j in xrange(1,len(str2)+1):  
            if str1[i-1] == str2[j-1]:  
                d = 0  
            else:  
                d = 1  
            matrix[i][j] = min(matrix[i-1][j]+1,matrix[i][j-1]+1,matrix[i-1][j-1]+d)  
  
  
    return matrix[len(str1)][len(str2)]  


if len(sys.argv) != 4 :
	print "Usage: " + sys.argv[0] + " [options] <lexiconp-txt> <data-text> <decode-tra> "
	print "e.g.: " + sys.argv[0] + " data/local/lang/lexiconp.txt data/test/text exp/tri3a_mfcc_pitch_dnn_nd4_hd1024/decode_test_lang_test/scoring/log/best_path.15.log"
	print "options: "
	print "			"
else :
	#讀入words與phones的對照表
	ifp = open(sys.argv[1], 'r')
	print "reading dict " + sys.argv[1] + "...."
	dict = {"init":"null"}
	
	while True:
		line = ifp.readline()
		if not line: 
			break
		list = re.split('\n|\t| ',line)
		reg = ""
		for i in range(3, len(list), 2) :
			reg += str(list[i][len(list[i])-1])
		dict[str(list[0])] = reg
			
	print "dict count:" + str(len(dict))
		
	ifp.close()
			
	#讀入正確答案 <data-text>
	ifp = open(sys.argv[2], 'r')
	print "reading text " + sys.argv[2] + "...."
	ans = {"init":"null"}
	key_list = {0:"null"} #紀錄所有key name
	index = 0
	
	while True:
		line = ifp.readline()
		if not line: 
			break
		list = re.split('\n| ',line)
		reg = ""
		for i in range(1, len(list)-1) :
			if list[i] != '':
				reg += str(dict[list[i]])
		ans[str(list[0])] = reg
		key_list[index] = str(list[0])
		index+=1
	ifp.close()
	
	#讀入辨識答案 <decode-tra>
	ifp = open(sys.argv[3], 'r')
	print "reading tra " + sys.argv[3] + "...."
	result = {"init":"null"}
	
	while True:
		line = ifp.readline()
		if not line: 
			break
		if line[0]=='#' or line[0:19]=="lattice-add-penalty" or line[0:13]=="lattice-scale" or line[0:17]=="lattice-best-path" or line[0:3]=="LOG" :
			#skip it
			donoting=0
		else :
			list = re.split('\n| ',line)
			reg = ""
			for i in range(1, len(list)-1) :
				if list[i] != '':
					reg += str(dict[list[i]])
			result[str(list[0])] = reg
	ifp.close()
	
	#開始比較tone error rate
	total_count=0
	error_count=0
	for i in range(0, len(key_list)) :
		error_count += edit(ans[key_list[i]],result[key_list[i]])
		total_count += len(ans[key_list[i]])
		
	print "total_count:" + str(total_count)
	print "error_count:" + str(error_count)
	tone_error_rate = (float(error_count)/float(total_count))*100
	print "tone_error_rate:" + str(round(tone_error_rate,2)) + "%"
			

	