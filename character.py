import actor
import defs
from tools import *

class Character(actor.Actor):
    def __init__(self, name = "unnamed"):
        actor.Actor.__init__(self, name)
        
        self.setProper(True)
        
        # position variables
        self.currentRoom = 0
        self.currentZone = 0
        self.client = None
        

    def getClient(self):
        return self.client

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
        
        if cz == "None" or cz == None:
            self.currentZone = None
            return True
        
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

    def isNameValid(self):
        
        # if blank line
        if self.getName() == "": return False
        
        for a in self.getName():
            
            chval = ord(a)
            
            if chval < ord('a') or chval > ord('z'):
                if chval < ord('A') or chval > ord('Z'):
                    return False
                    
        return True

    def saveToFile(self, tfile):
        
        fp = defs.CHARACTERS_PATH + tfile
        
        createNewFile(fp)
        
        f = open(fp, "w")
        
        clines = []
        
        # actor data
        clines += actor.Actor.saveToStrings(self)
        
        # save position data
        clines.append("%s_room:%d" %( self.getType(), self.getCurrentRoom()) )
        clines.append("%s_zone:%d" %( self.getType(), self.getCurrentZone()) )
        
        #write lines to file
        for line in clines:
            f.write("%s\n" %line)
        
        f.close()
        
    def loadFromFile(self, tfile):
        
        fp = defs.CHARACTERS_PATH + tfile
        
        if not fileExists(fp):
            print "Error, character file does not exist!"
            return False
        
        createNewFile(fp)
        
        # reset character to new
        #self = Character()
        
        # read each line in character file
        with open(fp, "r") as f:
            for line in f:
                
                # remove newline from line
                line = line[:-1]
                
                delim = line.find(':')
                key = line[:delim]
                val = line[delim+1:]
                
                # character specific data
                if key == "%s_room" %self.getType():
                    self.setCurrentRoom( int(val) )
                elif key == "%s_zone" %self.getType():
                    if val == "None":
                        self.setCurrentZone(None)
                    else:
                        self.setCurrentZone( int(val) )
                
                # else pass to actor string loader
                else:
                    actor.Actor.loadFromStrings(self,  [line] )


        
        f.close()
    
if __name__ == "__main__":
    
    import gameinit
    gameinit.gameInitTest()
    
    newchar = Character("Roland")
    newchar.setCurrentRoom(2)
    newchar.setCurrentZone(3)
    newchar.addNewItem("sword")
    
    # check valid name
    print "Creating character %s." %newchar.getName()
    if newchar.isNameValid():
        print "%s is a valid character name." %newchar.getName()
    else:
        print "%s is NOT a valid character name!" %newchar.getName()
        exit()
    
    newchar.show()
    
    # save character to file
    newchar.saveToFile("testchar.dat")

    # reset actor
    print "\nLoading character from file:"
    newchar2 = Character()
    newchar2.loadFromFile("testchar.dat")
    newchar2.show()


