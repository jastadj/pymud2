import server

#if __name__ == "__main__":
pymud_server = server.Server()
pymud_server.initServer()
pymud_server.startMainLoop()
pymud_server.shutdownServer()
