import defs
import worldobject
import command
import roomexit

from tools import *

class Room(worldobject.WorldObject):
    def __init__(self, name = "unnamed"):
        worldobject.WorldObject.__init__(self, name)
        
        self.setProper(True)
        
        self.descriptors = {}
        self.exits = []
        self.inventory = []
        self.mobs = []    
    
    def hasMob(self, tmob):
        if tmob in self.mobs:
            return True
        else:
            return False
    
    def getMobs(self):
        return self.mobs
        
    def addMob(self, tmob):
        if tmob == None:
            print "Error adding mob to room, mob is null!"
            return False
        
        try:
            self.mobs.append(tmob)
        except:
            print "Error adding mob to room!"
            return False
    
    def addNewMob(self, mstring):
        
        newmob = command.newMob(mstring)
        
        if newmob != None:
            self.mobs.append(newmob)
            return True
        
        else: return False    
            
    def removeMob(self, tmob):
        
        if tmob != None:
            print "Error removing mob from room, mob is null!"
            return False
        
        try:
            self.mobs.remove(tmob)
        except:
            print "Error removing mob from room!"
    
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
        newitem = command.newItem(istring)
        
        if newitem != None:
            self.inventory.append(newitem)
            return True
        
        else: return False
    
    def removeItem(self, titem):
        if titem == None:
            print "Error removing item from room, item is null!"
            return
        try:
            self.inventory.remove(titem)
        except:
            print "Error removing item from inventory"
    
    def addExit(self, exitname, roomnum, zonenum = None):
        
        # if zone num provided, check zone num is valid
        if zonenum != None:
            if zonenum < 0 or zonenum >= len(game.zones):
                print "Error adding exit to room, zone num %d out of range!" %zonenum
                return False
        
        newexit = roomexit.RoomExit(exitname, roomnum, zonenum)
        
        # check if room already has an exit by this name
        for e in self.exits:
            if e.getName() == exitname:
                print "Error adding exit to room, exit with name %s already exists!" %exitname
                return False
        
        # add new exit to room
        self.exits.append(newexit)
        
        return True
        
    def removeExit(self, exitname):
        
        # check if room exit by name exists
        for e in self.exits:
            if e.getName() == name:
                self.exits.remove(e)
                return True
        
        return False
    
    def isExit(self, exitname):
        
        # hardcode directional aliases for common dirs
        if exitname == "n":
            exitname = "north"
        elif exitname == "s":
            exitname = "south"
        elif exitname == "e":
            exitname = "east"
        elif exitname == "w":
            exitname = "west"
        
        # check if string is an exit string
        for e in self.exits:
            if e.getName() == exitname:
                return True
        return False
        
    def getExit(self, exitname):

        # hardcode directional aliases for common dirs
        if exitname == "n":
            exitname = "north"
        elif exitname == "s":
            exitname = "south"
        elif exitname == "e":
            exitname = "east"
        elif exitname == "w":
            exitname = "west"       
        
        for e in self.exits:
            if e.getName() == exitname:
                return e
        return None
    
    def getExits(self):
        return self.exits
    
    def addDescriptor(self, descdict):
        self.descriptors.update( descdict)
        
    def getDescriptors(self):
		return self.descriptors

    def saveToStrings(self):
        
        tstrings = []
        
        tstrings.append("room:%s" %self.getType() )
        
        # save base class data
        tstrings += worldobject.WorldObject.saveToStrings(self)
        
        # save room data
        
        # save descriptors
        for d in self.descriptors.keys():
            tstrings.append("%s_descriptor:%s:%s" %(self.getType(), d, self.descriptors[d]) )
        
        # save items
        for i in self.inventory:
            tstrings.append("%s_additem:%s" %(self.getType(), i.getExName() ) )
        
        # save mobs
        for m in self.mobs:
            tstrings.append("%s_addmob:%s" %(self.getType(), m.getExName() ) )
            
        # save exits
        for e in self.exits:
            rstrings = e.saveToStrings()
            # save exit strings prefixed with self type
            for s in rstrings:
                tstrings.append("%s_%s" %(self.getType(), s) )
        
        return tstrings

    def loadFromStrings(self, tstrings):
        
        # load base class data
        worldobject.WorldObject.loadFromStrings(self, tstrings)
        
        for line in tstrings:
            # process room exit line to room exit class
            if "%s_RoomExit"%self.getType() in line:
                try:
                    line = line.replace("%s_"%self.getType(), "", 1)
                    self.exits[-1].loadFromStrings([line])
                except:
                    print "Error processing room exit string, no room exits!"     
                 
                continue       
            
            delim = line.find(':')
            key = line[:delim]
            val = line[delim+1:]
            
            # descriptor
            if key == "%s_descriptor" %self.getType():
                ddelim = val.find(':')
                dkey = val[:ddelim]
                dval = val[ddelim+1:]

                self.addDescriptor( {dkey:dval} )
            
            # items
            elif key == "%s_additem" %self.getType():
                if not self.addNewItem(val):
                    print "ERROR ADDING NEW ITEM TO ROOM : %s" %val
            
            # mobs
            elif key == "%s_addmob" %self.getType():
                if not self.addNewMob(val):
                    print "ERROR ADDING NEW MOB TO ROOM : %s" %val
            
            # room exit
            elif key == "%s_roomexit"%self.getType():
                self.exits.append(roomexit.RoomExit())
            

                
                
    
    def show(self):
        
        worldobject.WorldObject.show(self)
        
        print "%d items" %len(self.inventory)
        print "%d mobs" %len(self.mobs)
        print "Descriptors #:%d" %len(self.descriptors.keys())
        if len(self.descriptors.keys()) != 0:
            for d in self.descriptors.keys():
                print "%s:%s" %(d, self.descriptors[d])
        
        print "Exits:"
        if len(self.exits) != 0:
            for e in self.exits:
                if e.getZoneNum() != None:
                    print "%s = %d (ZONE %d)" %(e.getName(), e.getRoomNum(), e.getZoneNum())
                else:
                    print "%s = %d" %(e.getName(), e.getRoomNum())
        else:
            print "No exits!"


        
        


if __name__ == "__main__":
    import gameinit
    gameinit.gameInitTest()
        
    newroom = Room("Treasury")
    newroom.setDescription("You are standing in a well fortified treasury.  A large iron gate with thick bars blocks your way to the south.")
    newroom.addExit("north", 1)
    newroom.addDescriptor( {"gate":"The gate looks nearly indestructable."} )
    newroom.addNewItem("sword")
    newroom.exits[-1].setDescription("A doorway to the north.")
    newroom.show()
    
    rstrings = newroom.saveToStrings()
    
    print "\nRoom Strings:"
    for line in rstrings:
        print line
        
    print "\nLoading room from strings..."
    newroom2 = Room()
    newroom2.loadFromStrings(rstrings)
    newroom2.show()
