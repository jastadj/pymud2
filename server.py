

import socket, select
import credential
import client
import item
import zone
import room
import command
import game
import handler

import login

from tools import *

class Server(object):
	def __init__(self):
				
		self.socket = None
		self.clients = []
		#0=uninit, 1=initialized, -1=shutdown
		self.status = 0 
		self.accounts = None
		
	def isRunning(self):
		if self.status == 1:
			return True
		else: return False
	
	def initServer(self):
		
		if self.isRunning():
			print "Unable to start server!"
			return False

		print "Starting server..."
		self.status = 1
		
		#create an INET, STREAMing socket
		self.socket = socket.socket(
			socket.AF_INET, socket.SOCK_STREAM)
		
		# bind locally on port
		self.socket.bind( ("0.0.0.0", 8888) )
		
		# listed on socket
		self.socket.listen(5)
		
		print "Socket is listening..."
		
		
		# callbacks
		game.server = self
		game.clients = self.clients
		game.ITEM = item.Item
		game.ROOM = room.Room
		game.ZONE = zone.Zone
		game.COMMAND = command.Command
		game.COMMAND_SET = command.CommandSet

		
		# load credentials
		credential.loadCredentials()
		print "%d accounts loaded." %len(game.credentials)
		
		# load common items
		item.loadItems()
		print "%d items loaded." % len(game.items)
		
		# load zones
		zone.loadZones()
		print "%d zones loaded." % len(game.zones)
		
		
		# init commands
		game.cmds_main = command.initMainCommands()
		game.invalidcmd = command.CommandSet.invalidcmd
		print "%d commands loaded." % game.cmds_main.count()
		
		return True
		
	def getAllSockets(self):
		if not self.isRunning():
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
		
		while self.isRunning():
			
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
					
					# configure client starting mode
					newclient.setMode("login1")
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
						self.status = -1
					
					# input is valid
					# now give client feedback
					handler.handleClient(tclient)
					
					
			

	def shutdownServer(self):			
		
		print "Shutting down server..."
		
		if self.status != -1:
			self.status = -1
		
		
		# save stuff
		credential.saveCredentials()
		print "Credentials saved."
		
		# save zones
		zone.saveZones()
		print "Zones and rooms saved."
		
		# shutdown and close server socket
		self.socket.shutdown(0)
		self.socket.close()
		self.socket = None

		
		return True




if __name__ == "__main__":
	testserver = Server()
	testserver.initServer()
	testserver.shutdownServer()
