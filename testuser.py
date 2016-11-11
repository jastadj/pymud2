from __future__ import print_function
# need future import to use python 3 print function

import client
import socket


class TestUser(client.Client):
	def __init__(self):
		self.last_input = ""
		self.mode = "maingame"
		self.current_room = 0
		self.current_zone = 0
		
		self.inventory = []
		
	def send(self, astr):
		print(astr, end="")
		



if __name__ == "__main__":
	tuser = TestUser()
	
	tuser.send("yo!")
	tuser.send("another test\n")
	
	print("TEST MODE=%s" %tuser.mode)
	
	
	
