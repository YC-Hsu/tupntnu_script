# -*- coding: utf-8 -*-
import sys,re,math,time

def CheckExist(list,str):
	for a in list :
		if a == str :
			return 'true'
	return 'flase'

def LPP(frame_posterior,phone,phone2pdf,Ts,Te): #log phone posterior probability
	result=0.0
	for i in range(Ts,Te) :
		senone=0.0
		for j in range(0,len(phone2pdf[phone])) :
			senone += frame_posterior[i][phone2pdf[phone][j]]
		result += math.log(senone)
	result /= float(Te - Ts)
	return result

def LPR(frame_posterior,phone1,phone2,phone2pdf,Ts,Te): #log phone posterior ratio
	p1 = LPP(frame_posterior,phone1,phone2pdf,Ts,Te)
	p2 = LPP(frame_posterior,phone2,phone2pdf,Ts,Te)
	p = p1 - p2
	return p
	
def Trans2U(str) :
	length = 4 - len(str)
	key = "U"
	for i in range(0,length) :
		key += '0'
	key += str
	return key

if len(sys.argv) != 7 :
	print "Usage: [python-command] " + sys.argv[0] + " [options] <phones-file> <MS-info> <transitions-state> <ali-file> <nnet-feats> <out-dir>"
	print "e.g.: python " + sys.argv[0] + " data/lang/phones.txt \\"
	print "\tdata/lang/tmp/state_and_phone.txt \\"
	print "\texp/mono0a_train_ali/tmp/mono0a_train_ali.txt \\"
	print "\texp/mono0a_train_ali/tmp/nnet.feats \\"
	print "\texp/MisPronunciation.txt "
	print "options: "
	print "			"
	exit()

#讀取phones.txt檔案
ifp = open(sys.argv[1], 'r')
phones=[]
while True:
	line = ifp.readline()
	if not line:
		break
	line_list = re.split(' |\n',line)
	if line_list[0][0] == '#' or line_list[0] == '<eps>' or line_list[0] == 'SIL' :
		time.sleep(0.001) #donothing
	else :
		phones.append(line_list[0])
print "phone dictionary have " + str(len(phones)) + " phones."

ifp = open(sys.argv[2],'r') # MS.info
ms_dict = {}
while True :
	line = ifp.readline()
	if not line :
		break
	line_list = re.split('\t|\n',line)
	
	key = Trans2U(line_list[1]) + "_" + line_list[6]
	if line_list[13] == 'X' or line_list[14] == 'X' :
		line_list[13] = 'F'
	elif line_list[13] == 'O' and line_list[14] == 'O' :
		line_list[13] = 'T'
	if line_list[12] == 'O':
		line_list[12] = 'T'
	elif line_list[12] == 'X':
		line_list[12] = 'F'
	reg = [line_list[2],line_list[0],line_list[10],line_list[12],line_list[13]]
	
	if ms_dict.get(key) == None :
		# [words,評音人,國籍,OX,OX(final & tone merge)]
		ms_dict[key] = reg
	else : # 優先順序為 1.Admin 2.劉珮君 3.熊玉雯
		if ms_dict[key][1] != "Admin" and line_list[0] == "Admin" :
			ms_dict[key] = reg
		elif ms_dict[key][1] != "劉姵君" and (line_list[0] == "Admin" or line_list[0] == "劉姵君") :
			ms_dict[key] = reg
		elif ms_dict[key][1] != "熊玉雯" and (line_list[0] == "Admin" or line_list[0] == "劉姵君" or line_list[0] == "熊玉雯") :
			ms_dict[key] = reg
ifp.close()
#print ms_dict


#讀取轉換每個frame對應到的state與phone所需的查詢表
ifp = open(sys.argv[3], 'r')
current_phone=''
current_pdf=0
current_state=0
index=0
phone_index=[]
phone2pdf={}
for i in range(0,10000) :
	phone_index.append([0,0,0,0,0])

while True:
	line = ifp.readline()
	if not line:
		break
	line_list = re.split(' |\n|\[|\]',line)
	if line_list[0] == 'Transition-state' :
		current_phone = str(line_list[4])
		current_pdf = int(line_list[10],10)
		current_state = int(line_list[7],10)
	elif line_list[1] == 'Transition-id' :
		index = int(line_list[3],10)
		phone_index[index][0] = current_phone
		phone_index[index][1] = current_pdf
		phone_index[index][2] = current_state
		if line_list[9] == '' :
			phone_index[index][3] = current_state #轉移到自己
		else :
			phone_index[index][3] = int(line_list[10]) #轉移到下一個狀態
		phone_index[index][4] = float(line_list[6]) #轉移機率
		# 建立phone2pdf的dictionary
		if phone2pdf.get(current_phone) == None and current_phone != 'SIL' :
			phone2pdf[current_phone] = []
		if current_phone != 'SIL' and CheckExist(phone2pdf[current_phone],current_pdf) == 'flase' :
			phone2pdf[current_phone].append(current_pdf)
			phone2pdf[current_phone].sort()
	else :
		time.sleep(0.001) #donothing
ifp.close()
print "alingment info have " + str(len(phone2pdf)) + " phones."

if len(phone2pdf) != len(phones) :
	print "[Error] file " + sys.argv[1] + " have " + str(len(phones)) + " phones, "
	print "[Error] file " + sys.argv[2] + " have " + str(len(phone2pdf)) + " phones."
	print "[Error] phones numbers mismatch!"
	exit()

#讀取alignment的訊息(ifp1)，以及Dnn posterior frame based的資訊(ifp2)，其維度與alignment的pdf相符
ifp1 = open(sys.argv[4], 'r')
ifp2 = open(sys.argv[5], 'r')
ofp = open(sys.argv[6] , 'w')
key_name=''
current_key =''
dimen=0
while True:
	line1 = ifp1.readline()
	if not line1:
		break
	line1_list = re.split(' |\n|\[|\]',line1)
	#===先計算line1中的空值的數量，再將其刪除===
	space = line1_list.count('')
	for i in range(0,space) :
		line1_list.remove('')
	#======================================
	#===記錄該key的每個frames的phone===
	key_frames_phone=[]
	print "key : " + str(line1_list[0])
	for i in range(1,len(line1_list)) :
		key_frames_phone.append(phone_index[int(line1_list[i])][0])
	print "key [" + str(line1_list[0]) + "] have " + str(len(key_frames_phone)) + " frames."
	#================================
	#debug
	#===ifp2第一次讀檔(要讀兩次因為key name與每個frame的feature都為不同行)===
	if key_name == '' :
		line2 = ifp2.readline()
		line2_list = re.split(' |\n|\[|\]',line2)
		key_name = line2_list[0]
	#=================================================================
	#debug
	#print line2_list[0]
	#===ifp2第二次讀檔，將每個frame的posterior都讀入後並轉換成softmax===
	frame_count=0
	frame_posterior=[]
	key_posterior=[]
	while True:
		line2 = ifp2.readline()
		line2_list = re.split(' |\n|\[|\]',line2)
		space = line2_list.count('')
		#print "[debug]" + str(len(line2_list))
		for i in range(0,space) :
			line2_list.remove('')
		#剛讀入該key的feats時還不知道維度，所以要記錄維度
		if dimen == 0 :
			dimen = len(line2_list)
			print "Model output dimension is " + str(dimen) + " ."
		if len(line2_list) != dimen:
			print "key [" + key_name + "] record done."
			current_key = key_name
			if len(line2_list) >= 1 :
				key_name = line2_list[0]
			break
		else :
			frame_posterior.append(line2_list)
			frame_count=frame_count+1
	print "frame count : " + str(frame_count)
	print "start to softmax ..."
	for i in range(0,len(frame_posterior)) :
		down=0.0
		for j in range(0,len(frame_posterior[i])) :
			down += math.exp(float(frame_posterior[i][j]))
		for j in range(0,len(frame_posterior[i])) :
			frame_posterior[i][j] = float(math.exp(float(frame_posterior[i][j])) / down)
	print "Done."
	print "Calculated " + str(len(frame_posterior)) + " frames."
	print "Create phone-level features ..."
	Fp=[]
	Ts=0
	Te=0
	syllable_index=0
	current_phone=''
	if len(frame_posterior) != len(key_frames_phone) :
		print "[Error] Array dimension doesn't match."
		print "[Error] alignment info have " + str(len(key_frames_phone)) + "frames."
		print "[Error] feats info have " + str(len(frame_posterior)) + "frames."
		print "[Error] exit this program. "
		exit()
	else :
		for i in range(0,len(frame_posterior)) :
			if i == 0 :
				current_phone=key_frames_phone[i]
				Ts = 0
			elif current_phone != key_frames_phone[i] : #表示phone的界限已經結束
				Te = i - 1
				if current_phone != 'SIL' :
					ofp.write(current_phone)
					ofp.write(" " + ms_dict[current_key][syllable_index+3])
					for j in range(0,len(phones)) :
						ofp.write(" " + str(LPP(frame_posterior,phones[j],phone2pdf,Ts,Te)))
					for j in range(0,len(phones)) :
						ofp.write(" " + str(LPR(frame_posterior,phones[j],current_phone,phone2pdf,Ts,Te)))
					ofp.write("\n")
					syllable_index+=1
				Ts = i
				current_phone=key_frames_phone[i]
			elif i == len(frame_posterior) - 1 : #表示到整句話的結尾，也需要做結束
				Te = i
				if current_phone != 'SIL' :
					ofp.write(current_phone)
					ofp.write(" " + ms_dict[current_key][syllable_index+3])
					for j in range(0,len(phones)) :
						ofp.write(" " + str(LPP(frame_posterior,phones[j],phone2pdf,Ts,Te)))
					for j in range(0,len(phones)) :
						ofp.write(" " + str(LPR(frame_posterior,phones[j],current_phone,phone2pdf,Ts,Te)))
					ofp.write("\n")
					syllable_index+=1
		print "Done."
ifp1.close()
ifp2.close()
ifp.close()
ofp.close()
