import os.path

from tools import *

rooms = []
rooms_filename = "./data/rooms.dat"
rooms_loaded = False

class Room(object):
	def __init__(self):
		self.name = "unnamed"
		self.desc = "no description"
		self.test = 0
	def show(self):
		print "Name:" + self.name
		print "Desc:" + self.desc
		print "Test:%d" % self.test


def load(altfile = None):
	if rooms_loaded:
		print "Rooms have already been loaded!"
		return False
	
	fp = rooms_filename
	
	# alternative file name provided?
	if altfile != None:
		fp = altfile
	
	# if file exists
	if os.path.isfile(fp):
		
		# config attributes
		dstr = ["name", "desc"]
		dint = ["test"]
		
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

			else:
				f.close()	
				
				return True
			
	else:
		return False

def save(altfile = None):
	
	fp = rooms_filename
	
	# alternative file name provided?
	if altfile != None:
		fp = altfile

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
		ofile.write("test:%d\n" % room.test)
		ofile.write("\n")
	
	ofile.close()
	
	return True

def getCurrentRoom(tclient):
	cr = tclient.current_room
	
	if cr < 0 or cr >= len(rooms):
		return None
	
	return rooms[cr]

def doLookRoom(tclient):
	troom = getCurrentRoom(tclient)
	
	if troom == None:
		tclient.send("Error, current room not valid!\n")
		return
		
	tclient.send("%s%s%s\n" % (setColor(COLOR_CYAN, True), troom.name, resetColor()) )
	tclient.send("\n" + troom.desc + "\n\n")


if __name__ == "__main__":
	
	room1 = Room()
	room1.name = "Bathroom"
	room1.desc = "This is a bathroom."
	room1.test = 5
	
	room2 = Room()
	room2.name = "Living Room"
	room2.desc = "Spacious living room."
	room2.test = 8
	
	rooms.append(room1)
	rooms.append(room2)
	
	if True:
		if save("testrooms.dat"):
			print "Rooms saved"
	
	print "Saved rooms:"
	for room in rooms:
		room.show()
		
	if False:
		if not load("testroofms.dat"):
			print "Load error!"
	
	if True:
		rooms = []
		print "Rooms cleared."
	
	print "\n"
	
	if True:
		if load("testrooms.dat"):
			print "Rooms loaded."
		else:
			print "Error loading room!"
	
	for room in rooms:
		room.show()
