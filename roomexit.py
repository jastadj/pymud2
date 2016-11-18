import worldobject

class RoomExit(worldobject.WorldObject):
	def __init__(self, name, room, zone = None):
        worldobject.WorldObject.__init__(self, name)
		
		self.roomnum = int(room)
		
		if zone != None:
			self.zonenum = int(zone)
		else:
			self.zonenum = None
	
	def getRoomNum(self):
		return self.room
	
	def getZoneNum(self):
		return self.zone
	
    def setRoomNum(self, roomnum):
        self.roomnum
    
    def setZoneNum(self, zonenum):
        self.zonenum = zonenum
        
    def saveToStrings(self):
        
        tstrings = []
        
        tstrings.append("roomexit:%s" %self.getType())
        
        # save base class data
        tstrings += worldobject.WorldObect.saveToStrings(self)
        
        tstrings.append("%s_roomnum:%d" %self.getRoomNum() )
        tstrings.append("%s_roomnum:%d" %self.getRoomNum() )

if __name__ == "__main__":
	pass
	
	
