import os.path
import room
import defs
import game
import command
from tools import *

class Zone(object):
    
    zoneiterator = 0
    
    def __init__(self):
        self.rooms = []
        self.zonefile = None
        
        
    def addRoom(self, troom):
        if troom == None:
            print "Error adding room, room is null!"
            return False
        
        self.rooms.append(troom)
        return True
        
    
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
            
            
            
            with open(fp, 'r') as f:
                for line in f:
                    ln = line[:-1]

                    if ln == "":
                        continue

                    # object entry found, create new
                    if ln == "ROOM:":
                        rooms.append(room.Room())
                    
                    # look for obj attributes
                    else:
                        sfind = ln.find(':')
                        if sfind >= 0:
                            key = ln[0:sfind]
                            val = ln[sfind+1:]
                        
                            if key in dstr:
                                setattr(rooms[-1], key, val)
                            elif key in dint:
                                setattr(rooms[-1], key, int(val))   
                            elif key == "exits":
                                elist = val.split(",")
                                for e in range(0, len(elist)):
                                    if elist[e] == "-1":
                                        rooms[-1].exits[e] = None
                                    else:
                                        rooms[-1].exits[e] = int(elist[e])
                            elif key == "descriptors":
                                dfind = val.find(':')
                                dkey = val[0:dfind]
                                dval = val[dfind+1:]
                                rooms[-1].descriptors.update({dkey, dval})
                            elif key == "additem":
								rooms[-1].addNewItem(val)
                                    

                else:
                    f.close()   
                    
                    self.rooms = rooms
                
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
        
        # write to file
        for room in self.rooms:
            ofile.write("\n")
            ofile.write("ROOM:\n")
            
            # save basic info
            ofile.write("name:%s\n" % room.name)
            ofile.write("desc:%s\n" % room.desc)
            
            #save descriptors:
            for d in room.descriptors.keys():
                ofile.write("descriptor:%s:%s\n" %(d, room.descriptors[d]))
            
            #save exits
            ofile.write("exits:")
            for e in range(0, len(room.exits) ):
                delim = ","
                if e is len(room.exits)-1:
                    delim = ""
                if room.exits[e] == None:
                    ofile.write("-1" + delim)
                else:
                    ofile.write("%d%s" %(room.exits[e], delim) )
            ofile.write("\n")
            #save items
            for i in room.inventory:
				ofile.write("additem:%s\n" %i.getDescName())
            
            ofile.write("\n")
        
        ofile.close()
        
        return True
            
def loadZones():
     
    zf = defs.ZONES_INDEX_FILE
    
    game.zones = []
    
    zonefiles = []
 
     # if file exists
    if createNewFile(zf) == None:
        
        
        #read in index files
        with open(zf, "r") as f:
            line = f.readline()
            
            if line != "":
                line = line[:-1]
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
    import item
    
    defs.configTestMode()
    
    game.zones = []
    item.loadItems()
    
    mode = 2
    
    if mode == 1:
        # create empty zone
        newzone = Zone()
        newzone.zonefile = "meadows.zn"
        newzone.addRoom(room.Room())
        newzone.rooms[-1].name = "room 1"
        newzone.addRoom(room.Room())
        newzone.rooms[-1].name = "room 2"    
        #add to zoneslist
        game.zones.append(newzone)
        #save zone list
        saveZones()
        newzone.show()
    
    if mode == 2:
        loadZones()
        game.zones[0].show()
    
    

    
    
    