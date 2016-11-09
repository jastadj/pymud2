import os.path
import room

class Zone(object):
    def __init__(self):
        self.rooms = []
        # add blank default room
        self.addRoom( room.Room())
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

    def load(self, zonefile):
        if not zonefile:
            print "Unable to load zone, no file provided!"
            return None
        
        self.zonefile = zonefile
        
        fp = zonefile
        
        rooms = []
        
        # if file exists
        if os.path.isfile(fp):
            
            # config attributes
            dstr = ["name", "desc"]
            dint = []
            # open file for reading
            ifile = open(fp, 'r')
            with open(fp, 'r') as f:
                for line in f:
                    ln = line[:-1]

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
                                    

                else:
                    f.close()   
                    
                    self.rooms = rooms
                
        else:
            print "%s zone file does not exist!" % fp
            return None

    def save(self):
        
        if self.zonefile == None:
            print "Unable to save zone, no file provided!"
            return False
        
        fp = self.zonefile

        # if directory doesnt exist, create one
        fdir = os.path.dirname(fp)
        if not os.path.isdir(fdir) and fdir != "":
            os.mkdir(fdir)

        # open file for writing
        ofile = open(fp, 'w')
        
        # write to file
        for room in self.rooms:
            ofile.write("ROOM:\n")
            ofile.write("name:%s\n" % room.name)
            ofile.write("desc:%s\n" % room.desc)
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
        
        ofile.close()
        
        return True
            
 def loadZones(zonelist, zoneindexfile):
	 
	zf = zoneindexfile
	zonelist = []
	 
	makenew = False
	 
	if zf == None:
		 print "Zone index file is null!"
		 return False
	
	if zonelist == None:
		print "Zone list is null!"
		return
	 
	# check to make sure data directory exists, if not, create it
	ddir = os.path.dirname(fp)
	if not os.path.isdir(ddir) and ddir != "":
		os.mkdir(ddir)
		makenew = True
	
	# check if zoneindex file exists
	if not makenew:
		if not os.path.isfile(zf):
			makenew = True
	
	# if making a new zone index and default zone file
	if makenew:
		# open file for writing
		f = open(zf, 'w')
	 
if __name__ == "__main__":
    import room
    
    myzone = Zone()
    
    myzone.addRoom( room.Room())
    myzone.addRoom( room.Room())
    myzone.zonefile = "testzone.dat"
    
    print "Added room to zone."
    myzone.show()
    
    print "Saving zone..."
    myzone.save()
    
    print "Clearing zone..."
    myzone.rooms = []
    
    print "Loading zones..."
    myzone.load("testzone.dat")
    
    for r in myzone.rooms:
		myzone.showRoom(r)
    
    
    
    
