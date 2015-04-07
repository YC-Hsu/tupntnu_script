# -*- coding: utf-8 -*-
import re,sys,os,math,cPickle,gzip
from sklearn import svm
from sklearn.externals import joblib

if len(sys.argv) != 4 :
	print "Usage: [python-command] " + sys.argv[0] + " [options] <phones-file> <pickle-dir> <corpus-test> "
	print "e.g.: python " + sys.argv[0] + " data/lang/phones.txt \\"
	print "\texp/PLFeats_train/pickle \\"
	print "\texp/PLFeats_test/phone_level_corpus.txt \\"
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
	ifp.close()

	pkl_dir = sys.argv[2]
	pickle = {}
	for root, dirs, files in os.walk(pkl_dir):
		for f in files:
			fname = re.split('\.', f)
			if pickle.get(fname[0]) == None :
				pickle[fname[0]] = []
	print "Have " + str(len(pickle)) + " pickles in dir " + sys.argv[2] + " ."


	reg_length = 300
	clf = {}
	if reg_length > len(phones) :
		reg_length = len(phones)
	print "Loading first " + str(reg_length) + " pickles ... "
	for i in range(0,reg_length) :
		if pickle.get(phones[i]) != None and clf.get(phones[i]) == None:
			clf[phones[i]] = joblib.load(pkl_dir + "/" + phones[i] + '.pkl')
	print "Done. "

	T_T=0.0001
	T_F=0.0001
	F_T=0.0001
	F_F=0.0001
	count=0
	ifp = open(sys.argv[3],'r')
	print "Start to predict ... "
	while True:
		skip_flag = 0
		line = ifp.readline()
		if not line:
			break
		line_list = re.split(' |\n',line)
		line_list.remove('')
		X = line_list[2:len(line_list)]
		if clf.get(line_list[0]) == None :
			if pickle.get(line_list[0]) == None :
				print "[Warning] phone " + line_list[0] + " didn't have pickle, skip it. "
				skip_flag = 1
			else :
				clf.popitem()
				clf[line_list[0]] = joblib.load(pkl_dir + "/" + line_list[0] + '.pkl')
		if skip_flag == 0 :
			count += 1
			Y = clf[line_list[0]].predict(X)
			if line_list[1] == 'T' and line_list[1] == Y[0] :
				T_T += 1
			elif line_list[1] == 'T' and line_list[1] != Y[0] :
				T_F += 1
			elif line_list[1] == 'F' and line_list[1] == Y[0] :
				F_F += 1
			elif line_list[1] == 'F' and line_list[1] != Y[0] :
				F_T += 1
			else :
				print line_list[1] + " " + str(Y[0])
				print "[Error] predict Y doesn't match corpus ans . "
				exit()
	print "Finish " + str(count) + " samples. "
	T_pre = round(float(T_T/(T_T+F_T)),4)
	T_rec = round(float(T_T/(T_T+T_F)),4)
	F_pre = round(float(F_F/(F_F+T_F)),4)
	F_rec = round(float(F_F/(F_F+F_T)),4)
	Acc = round(float((T_T+F_F)/(T_T+T_F+F_T+F_F)),4)
	print "T_T:"+str(round(T_T))+" T_F:"+str(round(T_F))+" F_T:"+str(round(F_T))+" F_F:"+str(round(F_F))
	print "Total    T-pre:"+str(T_pre)+" T-rec:"+str(T_rec)+" F-pre:"+str(F_pre)+" F-rec:"+str(F_rec)+" Acc::"+str(Acc)
	ifp.close()

