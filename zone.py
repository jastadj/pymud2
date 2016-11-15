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
        
    def setDesc(self, desc):
        self.desc = desc
    
    def addRoom(self, troom):
        if troom == None:
            print "Error adding room, room is null!"
            return False
        
        self.rooms.append(troom)
        return True
        
    
    def getName(self):
        return self.name
        
    def getDesc(self):
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
        print "Desc:%s" %self.getDesc()
        for r in self.rooms:
            print "%d - %s" %(self.getRoomNum(r), r.name)
    
    def showRoom(self, troom):
        rnum = self.getRoomNum(troom)
        
        if rnum == None:
            print "Unable to get room from zone, doesn't exist!"
            return
            
        print "Room #:%d" %rnum
        troom.show()

    def getAllClients(self):
        znum = None
        zusers = []
        
        for z in game.zones:
            if z == self:
                znum = game.zones.index(self)
        
        if znum == None:
            print "Error getting all clients in zone, zone not found!\n"
            return []
        
        for u in game.clients:
            if u.current_zone == znum:
                zusers.append(u)
        
        return zusers
        
        

    def load(self, zonefile):
        if not zonefile:
            print "Unable to load zone, no file provided!"
            return None
        
        self.zonefile = zonefile
        
        fp = defs.ZONES_PATH + zonefile
        
        rooms = []
        
        # if file exists
        if os.path.isfile(fp) != None:
            
            # config attributes
            dstr = ["name", "desc"]
            dint = []
            # open file for reading
            ifile = open(fp, 'r')
            
            # read mode, 0 = room lines, 1 = itemlines
            readmode = 0
            
            itemlines = []
            
            with open(fp, 'r') as f:
                for line in f:
                    ln = line[:-1]

                    if ln == "":
                        continue

                    if ln == "zone_name":
                        self.setName(val)
                    elif ln == "zone_desc":
                        self.setDesc(val)
                        
                    # object entry found, create new
                    elif ln == "ROOM:":
                        
                        # if was previously reading in item lines
                        # note: this really shouldn't happen, all items
                        #       should be read in first
                        if readmode == 1:
                            
                            # if there are item lines to process
                            if len(itemlines) != 0:
                                
                                # create new item from item lines
                                newitem = item.loadItemFromStrings(itemlines)
                                
                                # if new item was created, add to zone items
                                if newitem != None:
                                    self.items.append(newitem)
                                    # add new zone items to master items list
                                    game.items += self.items                                    
                                else:
                                    print "Error loading new item from zone"
                                # reset item lines
                                itemlines = []
                            # set readmode to read in room lines
                            readmode = 0
                        
                        # create new room
                        rooms.append(room.Room())
                    
                    elif ln == "ITEM:":
                        # change read mode to items
                        readmode = 1
                        
                        # if there are item lines to process
                        if len(itemlines) != 0:
                            
                            # create new item from item lines
                            newitem = item.loadItemFromStrings(itemlines)
                            
                            # if new item was created, add to zone items
                            if newitem != None:
                                self.items.append(newitem)
                                # add new zone items to master items list
                                game.items += self.items                                
                            else:
                                print "Error loading new item from zone"
                            
                            # reset item lines
                            itemlines = []
                        
                    # read in room lines
                    elif readmode == 0:
                        sfind = ln.find(':')
                        if sfind >= 0:
                            key = ln[0:sfind]
                            val = ln[sfind+1:]
                        
                            if key in dstr:
                                setattr(rooms[-1], key, val)
                            elif key in dint:
                                setattr(rooms[-1], key, int(val))   
                            elif key == "exit":
                                
                                # find exit name
                                edlim = val.find(',')
                                ename = val[:edlim]
                                
                                # find room num
                                val = val[edlim+1:]
                                edlim = val.find(',')
                                eroomnum = val[:edlim]
                                
                                # find zone num
                                val = val[edlim+1:]
                                ezonenum = val
                                if val == "None":
                                    ezonenum = None
                                else:
                                    ezonenum = int(val)
                                
                                newexit = roomexit.RoomExit(ename, eroomnum, ezonenum)
                                
                                rooms[-1].exits.append(newexit)
                                
                            elif key == "descriptor":
                                dfind = val.find(':')
                                dkey = val[0:dfind]
                                dval = val[dfind+1:]
                                rooms[-1].descriptors.update({dkey:dval})
                            elif key == "additem":
                                rooms[-1].addNewItem(val)
                            elif key == "addmob":
								rooms[-1].addNewMob(val)
                    
                    # read in item lines
                    elif readmode == 1:
                        itemlines.append(ln)

                # done reading in file
                f.close()   
                
                self.rooms = rooms
                
                # if there are item lines to process
                if len(itemlines) != 0:
                    # create new item from item lines
                    newitem = item.loadItemFromStrings(itemlines)
                    
                    # if new item was created, add to zone items
                    if newitem != None:
                        self.items.append(newitem)
                    else:
                        print "Error loading new item from zone"
                        
                    # reset item lines
                    itemlines = []                  
                
        else:
            print "%s zone file does not exist!" % fp
            return None

    def save(self):
        
        # if zone has no file specified, save as iterative default
        if self.zonefile == None:
            self.zonefile = "zone" + str(Zone.zoneiterator) + ".zn"
            Zone.zoneiterator += 1
            print "No zone file provided, saving as %s" %self.zonefile
        
        fp = defs.ZONES_PATH + self.zonefile
        
        # if file doesnt exist, create it
        createNewFile(fp)

        # open file for writing
        ofile = open(fp, 'w')
        
        # write zone data
        ofile.write("zone_name:%s\n" %self.getName())
        ofile.write("zone_desc:%s\n" %self.getDesc())
        
        # write zone items first
        for titem in self.items:
            itemlines = item.saveItemToStrings(titem)
            
            for iline in itemlines:
                ofile.write(iline)
                
        # write room data to file
        for room in self.rooms:
            #ofile.write("\n")
            ofile.write("ROOM:\n")
            
            # save basic info
            ofile.write("name:%s\n" % room.name)
            ofile.write("desc:%s\n" % room.desc)
            
            #save descriptors:
            for d in room.descriptors.keys():
                ofile.write("descriptor:%s:%s\n" %(d, room.descriptors[d]))
            
            #save exits
            for e in room.exits:
                # save room exit with zone number
                if e.getZoneNum() != None:
                    ofile.write("exit:%s,%d,%d\n" %(e.getName(), e.getRoomNum(), e.getZoneNum()) )
                # save room exit without zone number
                else:
                    ofile.write("exit:%s,%d,None\n" %(e.getName(), e.getRoomNum()) )
            
            #save items
            for i in room.inventory:
                ofile.write("additem:%s\n" %i.getDescName())
            
            ofile.write("\n")
        
        ofile.close()
        
        return True
            
def loadZones():
     
    zf = defs.ZONES_INDEX_FILE
    
    #debug
    #print "loading zone index file : %s" %zf
    
    game.zones = []
    
    zonefiles = []
 
     # if file exists
    if createNewFile(zf) == None:
        
        
        #read in index files
        with open(zf, "r") as f:
            
            for line in f:
                
                # trim new line
                if line[-1] == '\n':
                    line = line[:-1]
                
                # if line isn't blank, add it to zonefile list
                if line != "":
                    #print line
                    zonefiles.append(line)
            
        f.close()
                
        # load in each zone from file
        for zt in zonefiles:
            newzone = Zone()
            newzone.load(zt)
            game.zones.append(newzone)
    
    # else file is new, create defaults
    else:
        
        print "No zones present.  Creating default zone..."
        # create default zone and room
        newzone = Zone()
        newzone.addRoom( room.Room())
        newzone.zonefile = "default.zn"
        newzone.save()
        # add this zone to zonelist
        game.zones.append(newzone)
        
        # save zonelist
        saveZones()
    

        
def saveZones():
    
    zones = game.zones
    
    # if necessary, create new zone index file
    createNewFile(defs.ZONES_INDEX_FILE)
    
    # save each zone
    for z in zones:
        z.save()
        
    # write zone index file
    f = open(defs.ZONES_INDEX_FILE, "w")
    
    for z in zones:
        f.write(z.zonefile + "\n")
    f.close()
    
        
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
    newzone.addRoom(livingroom)
    
    game.zones = []
    game.zones.append(newzone)
    
    # save test zones
    print "Saving test zone..."
    #newzone.save()
    saveZones()
    
