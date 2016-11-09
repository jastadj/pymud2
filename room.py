import os.path

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
		for d in self.exits:
			print d
	def getRoomNum(self, rooms):
		if self in rooms:
			return rooms.index(self)
		else:
			return None


def load(roomsfile = None):
	if not roomsfile:
		print "Unable to load rooms, no file provided!"
		return None
	
	fp = roomsfile
	
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
					rooms.append(Room())
				
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
				
				return rooms
			
	else:
		print "%s does not exist." % fp
		return None

def save(rooms, roomsfile):
	
	if not roomsfile:
		print "Unable to save rooms, no file provided!"
		return False
	
	if not rooms:
		print "Unable to save rooms, no rooms list provided!"
		return False
	
	if type(rooms) != list:
		print "Rooms list parameter is not a list!"
		return False
	
	fp = roomsfile

	# if directory doesnt exist, create one
	fdir = os.path.dirname(fp)
	if not os.path.isdir(fdir) and fdir != "":
		os.mkdir(fdir)

	# open file for writing
	ofile = open(fp, 'w')
	
	# write to file
	for room in rooms:
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


if __name__ == "__main__":
	tests = {1:True, 2:True, 3:True, 4:True}
	rooms = []
	
	room1 = Room()
	room1.name = "Bathroom"
	room1.desc = "This is a bathroom."
	room1.exits[1] = 1
	
	room2 = Room()
	room2.name = "Living Room"
	room2.desc = "Spacious living room."
	room2.exits[0] = 0
	
	rooms.append(room1)
	rooms.append(room2)
	
	def myroomprint(troom):
		print "Room Num:%d" % troom.getRoomNum(rooms)
		troom.show()
	
	if tests[1]:
		if save(rooms, "testrooms.dat"):
			print "Rooms saved"

		for room in rooms:
			print "Room num:%d" % room.getRoomNum(rooms)
			myroomprint(room)
		print "Saved rooms:"
	

	
	if tests[3]:
		rooms = []
		print "\nRooms cleared.\n"
	
	
	if tests[4]:
		rooms = load("testrooms.dat")
		
		if rooms:
			print "Rooms loaded."
		else:
			print "Error loading room!"
	
	for room in rooms:
		myroomprint(room)
