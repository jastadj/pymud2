from __future__ import print_function
# need future import to use python 3 print function

import client
import socket


class TestUser(client.Client):
	def __init__(self):
		self.account_name = "testaccount"
		self.last_input = ""
		self.mode = "maingame"
		self.current_room = 0
		self.current_zone = 0
		
		self.inventory = []
		
	def getName(self):
		return self.account_name
		
	def send(self, astr):
		print(astr, end="")
	
	def show(self):
		
		print("name:%s" %self.account_name)
		print("last_input:%s" %self.last_input)
		print("mode:%s" %self.mode)
		print("current_zoom:%d" %self.current_room)
		print("current_zone:%d" %self.current_zone)



if __name__ == "__main__":
	tuser = TestUser()
	
	tuser.send("yo!")
	tuser.send("another test\n")
	
	print("TEST MODE=%s" %tuser.mode)
	
	tuser.show()
	
	
