
class RoomExit(object):
	def __init__(self, name, room, zone = None):
		self.name = name
		self.room = int(room)
		
		if zone != None:
			self.zone = int(zone)
		else:
			self.zone = None
	
	def getRoomNum(self):
		return self.room
	
	def getZoneNum(self):
		return self.zone
	
	def getName(self):
		return self.name

if __name__ == "__main__":
	pass
	
	
