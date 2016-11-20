import worldobject

class RoomExit(worldobject.WorldObject):
    def __init__(self, name = "unnamed exit", room = 0, zone = None):
        
        worldobject.WorldObject.__init__(self, name)
        
        self.roomnum = int(room)
        
        if zone != None:
            self.zonenum = int(zone)
        else:
            self.zonenum = None
    
    def getRoomNum(self):
        return self.roomnum
    
    def getZoneNum(self):
        return self.zonenum
    
    def setRoomNum(self, roomnum):
        self.roomnum = roomnum
    
    def setZoneNum(self, zonenum):
        self.zonenum = zonenum
    
    def show(self):
        worldobject.WorldObject.show(self)
        print "RoomNum=%d" %self.getRoomNum()
        if self.zonenum == None:
            print "ZoneNum=None"
        else: print "ZoneNum=%d" %self.getZoneNum()   
    
    def saveToStrings(self):
        
        tstrings = []
        
        tstrings.append("roomexit:%s" %self.getType())
        
        # save base class data
        tstrings += worldobject.WorldObject.saveToStrings(self)
        
        tstrings.append("%s_roomnum:%d" %(self.getType(), self.getRoomNum() ) )
        if self.getZoneNum() == None:
            tstrings.append("%s_zonenum:None" %(self.getType()) )
        else:
            tstrings.append("%s_zonenum:%d" %(self.getType(), self.getZoneNum() ) )
        
        return tstrings
        
    def loadFromStrings(self, tstrings):
        
        # load base class data
        worldobject.WorldObject.loadFromStrings(self, tstrings)
        
        for line in tstrings:
            delim = line.find(':')
            key = line[:delim]
            val = line[delim+1:]
            
            if key == "%s_roomnum" %self.getType():
                self.setRoomNum( int(val) )
            elif key == "%s_zonenum" %self.getType():
                if val == "None":
                    self.setZoneNum(None)
                else: self.setZoneNum( int(val) )         



if __name__ == "__main__":
    myexit = RoomExit("north", 1, None)
    myexit.show()
    
    tstrings = myexit.saveToStrings()
    print "Saving to strings:"
    for line in tstrings:
        print line
    
    print "\nLoading from strings..."
    myexit2 = RoomExit("shit", 3, 3)
    myexit2.loadFromStrings(tstrings)
    myexit2.show()
    myroomnum = myexit2.getRoomNum()
    
