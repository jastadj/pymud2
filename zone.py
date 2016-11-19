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
        
        Zone.zoneiterator += 1
        
        self.name = name
        self.description = "nodesc"
        self.rooms = []
        self.zonefile = None
        self.items = []
    
    def setFilename(self, fname):
        self.zonefile = fname
    
    def setName(self, name):
        self.name = name
        
    def setDescription(self, desc):
        self.description = desc
    
    def addRoom(self, troom):
        if troom == None:
            print "Error adding room, room is null!"
            return False
        
        self.rooms.append(troom)
        return True
    
    def getFilename(self):
        return self.zonefile
    
    def getName(self):
        return self.name
        
    def getDescription(self):
        return self.description
    
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
    
    def saveToFile(self, filename):
        
        # if no filename is set or provided, create
        # a default file name using zone iterator
        if filename == None:
            filename = "zone%d" %Zone.zoneiterator
            Zone.zoneiterator += 1
        
        # if a new file name is provided
        if filename != self.zonefile:
            self.zonefile = filename
        
        fp = defs.ZONES_PATH + filename
        
        #create file
        createNewFile(fp)
        
        f = open(fp, "w")
        
        
        # write zone header stuff
        f.write("zone_name:%s\n" %self.getName() )
        f.write("zone_description:%s\n"%self.getDescription() )
        f.write("\n")
        
        # write strings for each room to file
        for r in self.rooms:
            rstrings = r.saveToStrings()
            
            # write each room string to file
            for line in rstrings:
                f.write("%s\n" %line)
            
            # add space between rooms
            f.write("\n")
        
        f.close()
    
    def show(self):
        
        print "Zone Info:"
        print "Name:%s" %self.getName()
        print "Desc:%s" %self.getDescription()
        for r in self.rooms:
            print "%d - %s" %(self.getRoomNum(r), r.name)
                    
        
if __name__ == "__main__":
    
    import gameinit
    
    defs.configTestMode()
    
    # create test zone
    newzone = Zone("Billy's Apartment")
    newzone.setDescription("A pretty plain apartment.")
    newzone.zonefile = "apartment.zn"
    
    # create test zones
    bathroom = room.Room("Bathroom")
    bathroom.setDescription("You are standing in a bathroom that doesn't look like it has been maintained for some time.  The smells of stale urine fills your nose.  A grungry sink hangs precariously from the tiled wall.")
    bathroom.addExit("north", 1)
    newzone.addRoom(bathroom)
    
    livingroom = room.Room("Living Room")
    livingroom.setDescription("A pretty boring living room vacant of furniture.  Old posters are pinned lazily to the wall.")
    livingroom.addExit("south", 0)
    newzone.addRoom(livingroom)
    
    game.zones = []
    game.zones.append(newzone)
    
    # save test zones
    print "Saving test zone..."
    #newzone.save()
    gameinit.saveZones()
    
