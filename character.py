import actor
import defs
from tools import *

class Character(actor.Actor):
    def __init__(self):
        actor.Actor.__init__(self)
        
        self.iproperties.update({"currentroom":0})
        self.iproperties.update({"currentzone":0})      
        

    def getCurrentRoom(self):
        return self.iproperties["currentroom"]
        
    def getCurrentZone(self):
        return self.iproperties["currentzone"]
    
    def setCurrentRoom(self, cr):
        self.iproperties["currentroom"] = cr
        
    def setCurrentZone(self, cz):
        self.iproperties["currentzone"] = cz
        
    def show(self):
        print "Name  : %s" %self.getName()
        print "Desc  : %s" %self.getDesc()
        print "Zone  : %s" %self.getCurrentZone()
        print "Room  : %d" %self.getCurrentRoom()
        print "Items : %d" %len(self.getInventory())


def validCharacterName(tname):
    
    for a in tname:
        
        chval = ord(a)
        
        if chval < ord('a') or chval > ord('z'):
            if chval < ord('A') or chval > ord('Z'):
                return False
    
    return True

def saveCharacter(tchar, tfile):
    
    fp = defs.CHARACTERS_PATH + tfile
    
    createNewFile(fp)
    
    f = open(fp, "w")
    
    for s in tchar.sproperties:
        f.write("%s:%s\n" %(s, tchar.sproperties[s]) )
    
    for i in tchar.iproperties:
        f.write("%s:%d\n" %(i, tchar.iproperties[i]) )
        
    for i in tchar.getInventory():
        f.write("additem:%s\n" %i.getDescName())
    
    f.close()
    
def loadCharacter(tfile):
    
    fp = defs.CHARACTERS_PATH + tfile
    
    if not fileExists(fp):
        print "Error, character file does not exist!"
        return None
    
    createNewFile(fp)
    
    newcharacter = Character()
    
    # read each line in character file
    with open(fp, "r") as f:
        for line in f:
            
            # remove newline from line
            line = line[:-1]
            
            delim = line.find(':')
            
            key = line[:delim]
            val = line[delim+1:]
            
            if key in newcharacter.sproperties:
                newcharacter.sproperties[key] = val
            
            elif key in newcharacter.iproperties:
                newcharacter.iproperties[key] = int(val)
            elif key == "additem":
                newcharacter.addNewItem(val)
    f.close()
    
    return newcharacter
                
    
    
if __name__ == "__main__":
    
    charname = "john"
    
    if validCharacterName(charname):
        print "Name is valid!"
    else:
        print "ERROR!"
    


