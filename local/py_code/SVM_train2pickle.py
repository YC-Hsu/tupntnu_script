# -*- coding: utf-8 -*-
import sys,re,math,cPickle,gzip
from sklearn import svm
from sklearn.externals import joblib

if len(sys.argv) != 5 :
	print "Usage: [python-command] " + sys.argv[0] + " [options] <phones-file> <PLFeats-corpus> <tmp-file> <pickle-dir>"
	print "e.g.: python " + sys.argv[0] + " data/lang/phones.txt \\"
	print "\texp/PLFeats_train/phone_level_corpus.txt \\"
	print "\texp/PLFeats_train/corpus.tmp \\"
	print "\texp/PLFeats_train/pickle "
	print " "
	print "options: "
	print "			"
else :
	ifp = open(sys.argv[1],'r')
	phones=[]
	while True:
		line = ifp.readline()
		if not line:
			break
		line_list = re.split(' |\n',line)
		if line_list[0][0] == '#' or line_list[0] == '<eps>' or line_list[0] == 'SIL' :
			ssss=0 #donothing
		else :
			phones.append(line_list[0])
	print "phone dictionary have " + str(len(phones)) + " phones."
	
	# 讀取phone_level_corpus.txt檔案
	flag = 0
	index = 0
	out_while = 0
	steps = 30
	while True :
		phones_list = {}
		if out_while == 1 :
			break
		for i in range(index,index+steps) :
			if i < len(phones) :
				phones_list[phones[i]] = {}
				print "Search phone " + phones[i] + " ... "
			else :
				out_while = 1
				break
		
		if index == 0 :
			ifp = open(sys.argv[2], 'r')
		else :
			ifp = open(sys.argv[3] + str((flag+1)%2), 'r')
		ofp = open(sys.argv[3] + str(flag), 'w')
		while True:
			line = ifp.readline()
			if not line:
				break
			line_list = re.split(' |\n',line)
			line_list.remove('')
			if phones_list.get(line_list[0]) == None : #不屬於這次處理的對象（phone）
				ofp.write(line)
			else :
				if phones_list[line_list[0]].get(line_list[1]) == None :
					phones_list[line_list[0]][line_list[1]] = []
				phones_list[line_list[0]][line_list[1]].append(line_list[2:len(line_list)])
		flag = (flag+1) % 2
		ifp.close()
		ofp.close()

		
		for i in range(index,index+len(phones_list)) :
			if len(phones_list[phones[i]]) == 0 :
				print "Done. phone " + phones[i] + " have 0 sample. skip it."
			elif phones_list[phones[i]].get('T') == None :
				print "Done. phone " + phones[i] + " have 0 True sample. skip it."
			elif phones_list[phones[i]].get('F') == None :
				print "Done. phone " + phones[i] + " have 0 False sample. skip it."
			else :
				print "Start to SVM regression ... "
				X=[]
				Y=[]
				print "Phone [" + phones[i] + "] have " + str(len(phones_list[phones[i]]['T'])) + " True sample."
				for j in range(0,len(phones_list[phones[i]]['T'])) :
					X.append(phones_list[phones[i]]['T'][j])
					Y.append('T')
				print "Phone [" + phones[i] + "] have " + str(len(phones_list[phones[i]]['F'])) + " Flase sample."
				for j in range(0,len(phones_list[phones[i]]['F'])) :
					X.append(phones_list[phones[i]]['F'][j])
					Y.append('F')
				print "Start Phone [" + phones[i] + "] regression ... "
				clf = svm.SVC()
				msg = clf.fit(X, Y)
				print "====================\nmessage : \n====================\n" + str(msg) + "\n===================="
				print "Saving to pickle file ... "
				joblib.dump(clf, sys.argv[4] + "/" + phones[i] + ".pkl")
				print "Done."
			phones_list[phones[i]] = {}
		index += steps
