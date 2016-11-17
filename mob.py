import actor
import defs
import game
from tools import *

class Mob(actor.Actor):
    def __init__(self, name = "unnamed"):
        actor.Actor.__init__(self, name)


def saveMobToStrings(tmob):
    
    mstrings = []
    
    mstrings += actor.saveActorToStrings(tmob)
    
    return mstrings

def loadMobFromStrings(mstrings, tmob = None):
    
    newmob = None
    
    if newmob == None:
        newmob = Mob()
    
    alines = []
    
    for line in mstrings:
        
        lfind = line.find(':')
        key = line[:lfind]
        val = line[lfind+1:]
        
        if line.startswith("actor"):
            alines.append(line)
        elif line.startswith("noun"):
            alines.append(line)
            
    actor.loadActorFromStrings(alines, newmob)
    
    if tmob == None:
        return newmob

def saveMobs():
    
    fp = defs.MOBS_FILE
    
    createNewFile(fp)
    
    f = open(fp, "w")
    
    #write each mob's savestrings to file
    for m in game.mobs_common:
        
        mlines = saveMobToStrings(m)
        
        for line in mlines:
            f.write("%s\n" %line)
        
        f.write("\n")
    
    f.close()
        
def loadMobs():
    
    fp = defs.MOBS_FILE
    
    game.mobs_common = []
    
    # if file already exists
    if createNewFile(fp) == None:
        
        mlines = []
        
        # open file for reading
        with open(fp, "r") as f:
            
            # check each line in file
            for line in f:
                
                # trim new line
                line = line[:-1]
                
                # ignore blank lines
                if line != "":
                
                    # mob entry start
                    if line.startswith("mob_new"):
                        
                        # if mlines need to be processed
                        if len(mlines) != 0:
                            
                            # load mob
                            newmob = loadMobFromStrings(mlines)
                            
                            # add to working mob list
                            game.mobs_common.append(newmob)
                            
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
            game.mobs_common.append(newmob)
            mlines = []
    
        # append common mobs to main mobs list
        game.mobs += game.mobs_common
    
    # else file doesnt exist
    else:
        pass

if __name__ == "__main__":
    import gameinit
    
    # test save and load from mob file
    if True:
        gameinit.gameInitTest()
        
        if len(game.mobs) == 0:
            #create mob
            mob1 = Mob("Billy")
            print "New mob:"
            mob1.show()
            
            # add mob to main mob list
            game.mobs.append(mob1)
            
            # save mob file
            saveMobs()
        
        # print first mob
        print "Showing first loaded mob in list:"
        game.mobs[0].show()
    
    # test save and load strings
    if False:
        #create mob
        print "New mob:"
        mob1 = Mob("Billy")
        mob1.show()
        
        # saving mob to strings
        mstrings = saveMobToStrings(mob1)
        
        # create new mob and load from strings
        print "\nLoading new mob from strings"
        mob2 = loadMobFromStrings(mstrings)
        mob2.show()