import server

if __name__ == "__main__":
	
	pymudserver = server.Server()
	
	pymudserver.initServer()
	
	pymudserver.startMainLoop()
	
	pymudserver.shutdownServer()
