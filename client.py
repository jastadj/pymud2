import socket

class Client(object):
	REC_BUFFER = 4096
	
	def __init__(self, tsock):
		self.socket = tsock
		self.ip = tsock.getpeername()[0]
		self.port = int(tsock.getpeername()[1])
		self.account_name = None
		
		self.current_room = 0
		self.current_zone = 0
		
		# starting user mode
		self.mode = "login1"

		# skip next user input how many times?
		self.skip_input = 0

		# used to store temporary variables or input hist
		self.temp_var1 = ""
		self.temp_var2 = ""
		self.last_input = ""
	
	def send(self, msg):
		
		self.socket.send(msg);
	
	def receive(self):

		# try to receivee data
		try:
			# get input from client
			cdata = self.socket.recv(Client.REC_BUFFER)
			
			# if client data valid
			if cdata:
				# trim junk from cdata
				cdata = cdata[:-2]
				self.last_input = cdata
				return cdata
			
			# else data is not valid, something happened
			# like disconnect
			else:
				self.disconnect()
		 
		# client disconnected, so remove from socket list
		except:
			self.disconnect()
		
		# no valid data received, return nothing
		return None
	
	def disconnect(self):
		#close socket
		self.socket.close()
		

