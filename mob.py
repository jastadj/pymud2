import actor
import defs
import game
from tools import *

class Mob(actor.Actor):
    def __init__(self):
        actor.Actor.__init__(self)




def saveMobToStrings(tmob):
    
    mstrings = []
    
    # save string properties
    for s in tmob.sproperties.keys():
        mystrings.append("%s:%s\n" %(s, tmob.sproperties[s]) )
    
    # save int properties
    for i in tmob.iproperties.keys():
        mystrings.append("%s:%d\n" %(i, tmob.iproperties[i] ) )
    
    # save bool properties
    for b in tmob.bproperties.keys():
        mystrings.append("%s:%s\n" %(b, tmob.bproperties[b]) )
    
    # save inventory
    for titem in tmob.inventory():
        mystrings.append("additem:%s\n" %titem.getDescName() )
    
    return mstrings

def loadMobFromStrings(mstrings):
    
    newmob = Mob()
    

    for line in mstrings:
        
        lfind = line.find(':')
        key = line[:lfind]
        val = line[lfind+1:]
        
        # string properties
        if key in newmob.sproperties:
            newmob.sproperties.update( {key:val})
        
        # int properties
        elif key in newmob.iproperties:
            newmob.iproperties.update( {key:val})
        
        # bool properties
        elif key in newmob.bproperties:
            newmob.bproperties.update( {key:val})
        
    return newmob

def loadMobs():
    
    fp = defs.MOBS_FILE
    
    game.mobs = []
    
    # if file already exists
    if createNewFile(fp) == None:
        
        mlines = []
        mlist = []
        
        # open file for reading
        with open(fp, "r") as f:
            
            # check each line in file
            for line in f:
                
                # trim new line
                line = line[:-1]
                
                # ignore blank lines
                if line != "":
                
                    # mob entry start
                    if line == "MOB:":
                        
                        # if mlines need to be processed
                        if len(mlines) != 0:
                            
                            # load mob
                            newmob = loadMobFromStrings(mlines)
                            
                            # add to working mob list
                            mlist.append(newmob)
                            
                            # reset mob lines
                            mlines = []
                    
                    # add line to working mob lines
                    else:
                         mlines.append(line)
                        
        # done
        f.close()
    
        # process last mob entry
        if len(mlines) != 0:
            newmob = loadMobFromStrings(mlines)
            mlist.append(newmob)
            mlines = []
    
        #debug
        for m in mlist:
            print "ADDED MOB:%s" %m.getName()
    
        # append loaded modes to game mobs
        game.mobs += mlist
    
    # else file doesnt exist
    else:
        pass
