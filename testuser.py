from __future__ import print_function
# need future import to use python 3 print function

import client



class testuser(client.Client):
	def __init__(self):
		pass
	def send(self, astr):
		print(astr, end="")



if __name__ == "__main__":
	me = testuser()
	
	me.send("yo!")
	me.send("another test")
