import os

def unsplit(words):
    sentence = ""
    wcount = len(words)
    for word in words:
        sentence += word
        if word != words[-1]:
            sentence += " "
    return sentence


def getOppositeDirection(tdir):
	if tdir%2 == 0:
		return tdir+1
	else:
		return tdir-1

# define terminal colors
COLOR_BLACK = 0
COLOR_RED = 1
COLOR_GREEN = 2
COLOR_YELLOW = 3
COLOR_BLUE = 4
COLOR_MAGENTA = 5
COLOR_CYAN = 6
COLOR_WHITE = 7

TERM_ESCAPE = 0x1b

def resetColor():
	return "%c[%dm" % (TERM_ESCAPE, 0)

def setColor(tcolor, tbold = False):
	# esc[31m = red color
	# esc[31;1m = bold red color
	if not tbold:
		return "%c[%dm" %(TERM_ESCAPE, 30+tcolor)
	else:
		return "%c[%d;%dm" %(TERM_ESCAPE, 30+tcolor, 1)

def createNewFile(fp, create_dirs = False):
	
	if os.path.isfile(fp):
		#print "Error creating new file, already exists:%s" %fp
		return None
	
	# get file directory path
	fd = os.path.dirname(fp)
	
	# get directory tree list delim by /
	dtree = fd.split("/")
	
	# clean up relative paths
	for d in dtree:
		if d == "." or d == "..":
			dtree.remove(d)	
	
	# build directory tree
	dstring = "."
	for d in dtree:
		dstring += "/" + d
		if not os.path.isdir(dstring):
			os.mkdir(dstring)
	
	# create empty file
	newfile = open( fp, "w")
	newfile.close()
	
	return True
		

if __name__ == "__main__":
	
	if False:
		# test opposite directions
		testdirs = ["north","south","east","west"]
		for td in range(0, len(testdirs)):
			print "%d - %s" %(td, testdirs[td])
		
		mydir = 2
		print "opposite of %s is %s" %(testdirs[mydir], testdirs[getOppositeDirection(mydir)])
		
	createNewFile("./mytest/test1/john.txt")
	
