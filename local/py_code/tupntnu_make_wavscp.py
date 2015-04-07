# -*- coding: utf-8 -*-
import os,re,sys

if len(sys.argv) != 4 :
	print "Usage: " + sys.argv[0] + " [options] <text> <wav-scp> <corpus-dir>"
	print "e.g.: " + sys.argv[0] + " data/train/text data/train/wav.scp /mnt/corpus/TUP_NTNU/MS_WAV"
	print "options: "
	print "			"
	exit()

ifp = open(sys.argv[1], 'r')
ofp = open(sys.argv[2], 'w')
wav_dir = sys.argv[3]

while True :
	line = ifp.readline()
	if not line :
		break
	line_list = re.split(' |\n',line)
	ofp.write(line_list[0] + " " + wav_dir + "/" + line_list[0] + ".wav\n")

ifp.close()
ofp.close()
