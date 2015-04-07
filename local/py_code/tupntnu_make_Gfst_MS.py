import os,re,sys

if len(sys.argv) != 3 :
	print "Usage: " + sys.argv[0] + " [options] <words-txt> <lang-dir>"
	print "e.g.: " + sys.argv[0] + " data/lang/words.txt data/lang"
	print "options: "
	print "			"
	exit()

ifp = open(sys.argv[1], 'r')
ofp = open(sys.argv[2]+"/G.txt", 'w')
words = {}

while True :
	line = ifp.readline()
	if not line :
		break
	line_list = re.split(' |\n',line)
	if line_list[0][0] != '<' and line_list[0][0] != '#' :
		if words.get(line_list[0]) == None :
			words[line_list[0]] = -1
ifp.close()

words_list = words.items()

ofp.write("0\t1\t<eps>\t<eps>\n")

start=2
for i in range(0,len(words_list)) :
	ofp.write("1\t"+str(start)+"\t"+words_list[i][0]+"\t"+words_list[i][0]+"\t0\n")
	start+=1
end=2
for i in range(0,len(words_list)) :
	ofp.write(str(end)+"\t"+str(start)+"\t<eps>\t<eps>\n")
	end+=1
ofp.write(str(start))

ofp.close()