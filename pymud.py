import server

if __name__ == "__main__":
	pymud_server = server.Server()

	pymud_server.initServer()
	
	# load user credentials
	pymud_server.credentials.load()
	print "Loaded %d credentials." % len(pymud_server.credentials.credentials.keys())
	
	pymud_server.startMainLoop()

	pymud_server.shutdownServer()
