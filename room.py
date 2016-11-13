from tools import *

import defs
import game
import command

class Room(object):
    def __init__(self):
        self.name = "unnamed"
        self.desc = "no description"
        self.descriptors = {}
        self.exits = []
        self.zoneexits = {}
        self.inventory = []
        for a in range(0, len(defs.DIRECTIONS) ):
            self.exits.append(None)
        
    
    def test(self):
        print "test"
    
    def getAllClients(self):
        
        znum = None
        rnum = None
        
        ulist = []
        
        # check zones for this room
        for z in game.zones:
            rnum = z.getRoomNum(self)
            if rnum != None:
                znum = game.zones.index(z)
                break
        
        # room was not found in any zones
        if rnum == None:
            print "Room : get all clients, none found!"
            return []
        
        # check each user that matches zone and room num
        for u in game.clients:
            if u.char.getCurrentZone() == znum and u.char.getCurrentRoom() == rnum:
                ulist.append(u)
        
        if len(ulist) == 0:
            print "No users found in room"
        
        return ulist    
    
    def hasItem(self, titem):
        if titem in self.inventory:
            return True
        else:
            return False
    
    def getItems(self):
        return self.inventory
    
    def addItem(self, titem):
        if titem == None:
            print "Error adding item to room, item is null!"
            return
            
        try:
            self.inventory.append(titem)
        except:
            print "Error adding item to room!"
    
    def addNewItem(self, istring):
        newitem = command.getNewItem(istring)
        
        if newitem != None:
            self.inventory.append(newitem)
    
    def removeItem(self, titem):
        if titem == None:
            print "Error removing item from room, item is null!"
            return
        try:
            self.inventory.remove(titem)
        except:
            print "Error removing item from inventory"
    
    def show(self):
        print "Name:" + self.name
        print "Desc:" + self.desc
        print "%d items" %len(self.inventory)
        print "Descriptors:"
        if len(self.descriptors.keys()) == 0:
            print "None"
        else:
            for d in self.descriptors.keys():
                print "%s:%s" %(d, self.descriptors[d])
        
        print "Exits:"
        for a in range(0, len(defs.DIRECTIONS) ):
            if self.exits[a] == None:
                print "%s:%s" % (defs.DIRECTIONS[a], "None")
            else:
                if a in self.zoneexits.keys():
                    print "%s:%d (ZONE EXIT)" % (defs.DIRECTIONS[a], self.exits[a])
                else:
                    print "%s:%d" % (defs.DIRECTIONS[a], self.exits[a])
    
        
        


if __name__ == "__main__":
    
    import zone
    
    myzone = zone.Zone()
    
    
    tests = {1:True, 2:True, 3:True, 4:True}
    
    room1 = Room()
    room1.name = "Bathroom"
    room1.desc = "This is a bathroom that has a sink."
    room1.exits[1] = 1
    room1.descriptors.update({"sink":"It's just a plain old sink."})
    
    room2 = Room()
    room2.name = "Living Room"
    room2.desc = "Spacious living room."
    room2.exits[0] = 0
    
    myzone.addRoom(room1)
    myzone.addRoom(room2)
    
    
    def myRoomShow(troom):
        print "Room #%d" % myzone.getRoomNum(troom)
        troom.show()
    
    myzone.rooms[0].show()
        
