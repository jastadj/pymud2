import os.path
import room
import defs
import game
import command
import roomexit
import item
from tools import *

class Zone(object):
    
    zoneiterator = 0
    
    def __init__(self, name = "unnamed"):
        self.name = name
        self.desc = "nodesc"
        self.rooms = []
        self.zonefile = None
        self.items = []
    
    def setName(self, name):
        self.name = name
        
    def setDescription(self, desc):
        self.desc = desc
    
    def addRoom(self, troom):
        if troom == None:
            print "Error adding room, room is null!"
            return False
        
        self.rooms.append(troom)
        return True
        
    
    def getName(self):
        return self.name
        
    def getDescription(self):
        return self.desc
    
    def getRoomNum(self, troom):
        if troom in self.rooms:
            return self.rooms.index(troom)
        else:
            return None
    
    def getRoom(self, rnum):
        if rnum < 0 or rnum >= len(self.rooms):
            print "Unable to get room, index out of range!"
            return
        return self.rooms[rnum]
    
    def show(self):
        
        print "Zone Info:"
        print "Name:%s" %self.getName()
        print "Desc:%s" %self.getDescription()
        for r in self.rooms:
            print "%d - %s" %(self.getRoomNum(r), r.name)
                    
        
if __name__ == "__main__":
    
    defs.configTestMode()
    
    # create test zone
    newzone = Zone("Billy's Apartment")
    newzone.setDesc("A pretty plain apartment.")
    newzone.zonefile = "apartment.zn"
    
    # create test zones
    bathroom = room.Room("Bathroom")
    bathroom.setDesc("You are standing in a bathroom that doesn't look like it has been maintained for some time.  The smells of stale urine fills your nose.  A grungry sink hangs precariously from the tiled wall.")
    bathroom.addExit("north", 1)
    newzone.addRoom(bathroom)
    
    livingroom = room.Room("Living Room")
    livingroom.setDesc("A pretty boring living room vacant of furniture.  Old posters are pinned lazily to the wall.")
    livingroom.addExit("south", 0)
    livingroom.addNewMob("billy")
    newzone.addRoom(livingroom)
    
    game.zones = []
    game.zones.append(newzone)
    
    # save test zones
    print "Saving test zone..."
    #newzone.save()
    saveZones()
    
