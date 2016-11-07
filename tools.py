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

if __name__ == "__main__":
	
	# test opposite directions
	testdirs = ["north","south","east","west"]
	for td in range(0, len(testdirs)):
		print "%d - %s" %(td, testdirs[td])
	
	mydir = 2
	print "opposite of %s is %s" %(testdirs[mydir], testdirs[getOppositeDirection(mydir)])
		
