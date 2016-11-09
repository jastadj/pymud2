from tools import *

import defs

class Room(object):
    def __init__(self):
        self.name = "unnamed"
        self.desc = "no description"
        
        self.exits = []
        for a in range(0, len(defs.DIRECTIONS) ):
            self.exits.append(None)
    def show(self):
        print "Name:" + self.name
        print "Desc:" + self.desc
        
        for a in range(0, len(defs.DIRECTIONS) ):
            if self.exits[a] == None:
                print "%s:%s" % (defs.DIRECTIONS[a], "None")
            else:
                print "%s:%d" % (defs.DIRECTIONS[a], self.exits[a])



if __name__ == "__main__":
    
    import zone
    
    myzone = zone.Zone()
    
    
    tests = {1:True, 2:True, 3:True, 4:True}
    
    room1 = Room()
    room1.name = "Bathroom"
    room1.desc = "This is a bathroom."
    room1.exits[1] = 1
    
    room2 = Room()
    room2.name = "Living Room"
    room2.desc = "Spacious living room."
    room2.exits[0] = 0
    
    myzone.addRoom(room1)
    myzone.addRoom(room2)
    
    
    def myRoomShow(troom):
        print "Room #%d" % myzone.getRoomNum(troom)
        troom.show()
    
    for r in myzone.rooms:
        myRoomShow(r)
        
