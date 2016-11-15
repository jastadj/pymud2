import os
import random

# define terminal colors
COLOR_BLACK = 0
COLOR_RED = 1
COLOR_GREEN = 2
COLOR_YELLOW = 3
COLOR_BLUE = 4
COLOR_MAGENTA = 5
COLOR_CYAN = 6
COLOR_WHITE = 7

DISABLE_COLOR = True
TERM_ESCAPE = 0x1b

def resetColor():
    if DISABLE_COLOR: return ""
    return "%c[%dm" % (TERM_ESCAPE, 0)

def setColor(tcolor, tbold = False):
    # esc[31m = red color
    # esc[31;1m = bold red color
    if DISABLE_COLOR: return ""
    if not tbold:
        return "%c[%dm" %(TERM_ESCAPE, 30+tcolor)
    else:
        return "%c[%d;%dm" %(TERM_ESCAPE, 30+tcolor, 1)

def fileExists(fp):
    return os.path.isfile(fp)

def createNewFile(fp):
    
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

def fitStringToWidth(s, width = 80):
    
    lines = []
    
    #print "Length of string=%d" %len(s)
    
    if len(s) < width:
        return [s]
    
    while len(s) > width:
        
        if s[width-1] == " ":
            lines.append( s[:width])
            s = s[width:]
        else:
            for c in range(1, width):
                if s[width-1-c] == " ":
                    lines.append( s[:width-c])
                    s = s[width-c:]
                    break
                elif c == width-1:
                    lines.append( s[:width])
                    s = s[width:]
                    break

        

    # add leftover
    lines.append(s)
    
    return lines
            
class Dice(object):
    def __init__(self, rnum=1, rsides=6, rmod=0):
        self.num = rnum
        self.sides = rsides
        self.mod = rmod
    
    def roll(self):
        tot = 0
        
        for s in range(0, self.num):
            tot += random.randint(1, self.sides)
        
        tot += self.mod
        return tot
    
def rollDice(num=1, sides = 6, mod = 0):
    tot = 0
    
    for s in range(0, num):
        tot += random.randint(1, sides)
    
    tot += mod
    
    return tot

if __name__ == "__main__":
    
    if False:
        # test opposite directions
        testdirs = ["north","south","east","west"]
        for td in range(0, len(testdirs)):
            print "%d - %s" %(td, testdirs[td])
        
        mydir = 2
        print "opposite of %s is %s" %(testdirs[mydir], testdirs[getOppositeDirection(mydir)])
        
    createNewFile("./mytest/test1/john.txt")
        
    teststr = "this is a test.  testing that strings can be written out formatted to a specifically set width, mainly by 80 characters by default"
    p = fitStringToWidth(teststr)
    print teststr
    print "\n\n"
    for l in p:
        print l
    
    print "dice roll = %d" %rollDice()
