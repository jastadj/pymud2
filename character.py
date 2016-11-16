import actor
import defs
from tools import *

class Character(actor.Actor):
    def __init__(self):
        actor.Actor.__init__(self)
        
        # position variables
        self.currentRoom = 0
        self.currentZone = 0
        

    def getCurrentRoom(self):
        return self.currentRoom
        
    def getCurrentZone(self):
        return self.currentZone
    
    def setCurrentRoom(self, cr):
        try:
            newroom = int(cr)
            self.currentRoom = newroom
            return True
        except:
            print "Error setting character current room, val not int"
            return False
        
    def setCurrentZone(self, cz):
        try:
            newzone = int(cz)
            self.currentZone = newzone
            return True
        except:
            print "Error setting character current zone, val not int"
            return False
        
    def show(self):
        actor.Actor.show(self)
        print "Zone..........: %d" %self.getCurrentZone()
        print "Room..........: %d" %self.getCurrentRoom()        


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
    
    clines = []
    
    # actor data
    clines += actor.saveActorToStrings(tchar)
    
    # save position data
    clines.append("character_room:%d" %tchar.getCurrentRoom())
    clines.append("character_zone:%d" %tchar.getCurrentZone())
    
    #write lines to file
    for line in clines:
        f.write("%s\n" %line)
    
    f.close()
    
def loadCharacter(tfile):
    
    fp = defs.CHARACTERS_PATH + tfile
    
    if not fileExists(fp):
        print "Error, character file does not exist!"
        return None
    
    createNewFile(fp)
    
    newcharacter = Character()
    alines = []
    
    # read each line in character file
    with open(fp, "r") as f:
        for line in f:
            
            # remove newline from line
            line = line[:-1]
            
            delim = line.find(':')
            
            key = line[:delim]
            val = line[delim+1:]
            
            if key == "character_room":
                newcharacter.currentRoom = int(val)
            elif key == "character_zone":
                newcharacter.currentZone = int(val)
            else:
                alines.append(line)
    f.close()
    
    actor.loadActorFromStrings(alines, newcharacter)
    
    return newcharacter
                
    
    
if __name__ == "__main__":
    
    charname = "john"
    
    if validCharacterName(charname):
        print "Name is valid!"
    else:
        print "ERROR!"
    


