import socket
import select
import client
import handler
import game
import login
import credential
from tools import *






class Server(object):
	server_started = False
	server_shutdown = False
	def __init__(self):
		
		self.socket = None
		self.clients = []
		
	def initServer(self):
		
		if Server.server_started:
			print "Unable to start server, already running!"
			return False

		print "Starting server..."
		
		#create an INET, STREAMing socket
		self.socket = socket.socket(
			socket.AF_INET, socket.SOCK_STREAM)
		
		# bind locally on port
		self.socket.bind( ("0.0.0.0", 8888) )
		
		# listed on socket
		self.socket.listen(5)
		
		print "Socket is listening..."

		Server.server_started = True
		
		return True
		
	def getAllSockets(self):
		if not Server.server_started:
			print "Unable to get all sockets, server is not running!"
			return None
		
		# socket list
		slist = []
		
		# add server socket
		slist.append(self.socket)
		
		# add all client sockets
		for cnt in self.clients:
			slist.append( cnt.socket)
		
		
		return slist

	def getClient(self, tsocket):
		
		# look and return client with target socket
		for tclient in self.clients:
			if tsocket == tclient.socket:
				return tclient
		
		# not found, return None
		return None

	def startMainLoop(self):
		
		while not Server.server_shutdown:
			
			# get sockets with selector
			try:
				read_sockets,write_sockets,error_sockets = select.select( self.getAllSockets(),[],[])
			except:
				pass
			
			for tsock in read_sockets:
				
				# if server has something to do (new connection?)
				if tsock == self.socket:
					
					# get accepted new connection socket
					newsock, addr = self.socket.accept()
					
					# create new client
					newclient = client.Client(newsock)
					
					# add new client to list
					self.clients.append(newclient)
					print "Client %s:%d connected." %(newclient.ip, newclient.port)
					
					#print WELCOME screen
					newclient.send("\n%sWelcome!%s\n\n" %(setColor(COLOR_GREEN, True),
														resetColor()) )
					newclient.send("login:")
				
				# else a client has something to do
				else:
					
					tclient = self.getClient(tsock)
					
					if tclient == None:
						print "Error finding client with target socket!"
						print "Closing socket..."
						tsock.close()
						continue
							
					# receive client data
					cdata = tclient.receive()
					
					# if unable to receive data, something went wrong
					if cdata == None:
						# remove client from list
						print "Client %s:%d disconnected." %(tclient.ip, tclient.port)
						self.clients.remove(tclient)
						continue
					
					# debug
					if cdata == "shutdown":
						tclient.send("Commanded server shutdown.\n")
						Server.server_shutdown = True
					
					# input is valid
					# now give client feedback
					handler.handleClient(tclient)
					
					
			

	def shutdownServer(self):
		
		if not Server.server_started:
			print "Unable to shutdown, server is not running!"
			return False
			
		print "Shutting down server..."
		
		# shutdown and close server socket
		self.socket.shutdown(0)
		self.socket.close()
		self.socket = None
		
		Server.server_start = False
		Server.server_shutdown = False
		
		return True

