import server
import credential

#if __name__ == "__main__":
pymud_server = server.Server()

pymud_server.initServer()

# load user credentials
credential.credentials.load()
print "Loaded %d credentials." % len(credential.credentials.credentials.keys())

pymud_server.startMainLoop()

pymud_server.shutdownServer()
