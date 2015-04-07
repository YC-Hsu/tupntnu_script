import re,sys,time
if len(sys.argv) != 4 :
	print "Usage: [python-command] " + sys.argv[0] + " [options] <phones-file> <corpus-file> <threshold-file> "
	print "e.g.: python " + sys.argv[0] + " data/lang/phones.txt \\"
	print "\texp/PLFeats_dev/phone_level_corpus.txt \\"
	print "\texp/PLFeats_dev/phone_level_corpus_gop.txt"
	print ""
	print "options: "
	print "                 "
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

	ifp = open(sys.argv[2],'r')
	phone2gop={}
	while True:
		line = ifp.readline()
		if not line:
			break
		line_list = re.split(' |\n',line)
		line_list.remove('')
		if phone2gop.get(line_list[0]) == None :
			phone2gop[line_list[0]] = {}
		if phone2gop[line_list[0]].get(line_list[1]) == None :
			phone2gop[line_list[0]][line_list[1]] = []
		index=0
		for i in range(0,len(phones)) :
			if line_list[0] == phones[i] :
				index = i
				break;
		#if float(line_list[2+index]) > 0 or float(max(line_list[2:len(phones)+2])) > 0 :
			#print "[" + line_list[0] + "][" + line_list[2+index] + "][" + max(line_list[2:len(phones)+2]) + "]"
		phone2gop[line_list[0]][line_list[1]].append(float(line_list[2+index])-float(max(line_list[2:len(phones)+2])))
		phone2gop[line_list[0]][line_list[1]].sort(reverse = True)
	ifp.close()
	
	T_T=0.0
	T_F=0.0
	F_T=0.0
	F_F=0.0	
	ofp = open(sys.argv[3],'w')
	for i in range(0,len(phones)) :
		if phone2gop.get(phones[i]) == None :
			#print "phone " + phones[i] + " have 0 sample."
			time.sleep(0.001)
		else :
			#print "phone " + phones[i] + " have " + str(len(phone2gop[phones[i]]['T'])+len(phone2gop[phones[i]]['F'])) + " sample. (True+Flase)"
			time.sleep(0.001)
			list = []
			for j in range(0,len(phone2gop[phones[i]]['T'])) :
				list.append(phone2gop[phones[i]]['T'][j])
			for j in range(0,len(phone2gop[phones[i]]['F'])) :
                                list.append(phone2gop[phones[i]]['F'][j])
			m=-1
			n=-1
			for j in range(0,len(list)-1) :
				if list[j] < list[j+1] :
					for k in range(1,len(list)) :
						if j-k >= 0 and j+1+k < len(list) :
							if list[j-k] < list[j+1+k] :
								m=j-k
								n=j+1+k
							else :
								break
						else :
							m=j-k+1
							n=j+1+k-1
			threshold = 0.0
			if m==-1 and n==-1 :
				threshold = (float(phone2gop[phones[i]]['T'][len(phone2gop[phones[i]]['T'])-1]) + float(phone2gop[phones[i]]['F'][0])) / 2
			else :
				list_part = list[m:n]
				for j in range(0,len(list_part)) :
					threshold += float(list_part[j])
				threshold /= len(list_part)
			t_t = 0.0
			t_f = 0.0
			f_t = 0.0
			f_f = 0.0
			for j in range(0,len(phone2gop[phones[i]]['T'])) :
				if phone2gop[phones[i]]['T'][j] >= threshold :
					t_t += 1
				else :
					t_f += 1
			for j in range(0,len(phone2gop[phones[i]]['F'])) :
				if phone2gop[phones[i]]['F'][j] < threshold :
					f_f += 1
				else :
					f_t += 1
			T_pre = round(float(t_t/(t_t+f_t)),2)
			T_rec = round(float(t_t/(t_t+t_f)),2)
			F_pre = round(float(f_f/(f_f+t_f)),2)
			F_rec = round(float(f_f/(f_f+f_t)),2)
			Acc = round(float((t_t+f_f)/(t_t+t_f+f_t+f_f)),2)
			T_T += t_t
			T_F += t_f
			F_T += f_t
			F_F += f_f
			ofp.write(phones[i]+" "+str(threshold)+" "+str(T_pre)+" "+str(T_rec)+" "+str(F_pre)+" "+str(F_rec)+" "+str(Acc)+"\n")

	T_pre = round(float(T_T/(T_T+F_T)),2)
	T_rec = round(float(T_T/(T_T+T_F)),2)
	F_pre = round(float(F_F/(F_F+T_F)),2)
	F_rec = round(float(F_F/(F_F+F_T)),2)
	Acc = round(float((T_T+F_F)/(T_T+T_F+F_T+F_F)),2)
	print "T_T:"+str(round(T_T))+" T_F:"+str(round(T_F))+" F_T:"+str(round(F_T))+" F_F:"+str(round(F_F))
	print "Total    T-pre:"+str(T_pre)+" T-rec:"+str(T_rec)+" F-pre:"+str(F_pre)+" F-rec:"+str(F_rec)+" Acc::"+str(Acc)
	ofp.close()
