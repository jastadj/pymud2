import server
import credential
import room

#if __name__ == "__main__":
pymud_server = server.Server()

pymud_server.initServer()

# load user credentials
credential.credentials.load()
print "Loaded %d credentials." % len(credential.credentials.credentials.keys())

# load rooms
if not room.load():
	# if no rooms file, create blank
	room.rooms.append( room.Room())

print "Room count:%d" % len(room.rooms)

pymud_server.startMainLoop()

pymud_server.shutdownServer()

# save credential file
print "Saving credentials..."
credential.credentials.save()

# save rooms
print "Saving rooms..."
room.save()
