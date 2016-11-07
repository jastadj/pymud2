import client

def loginMenu(tclient):
	
	if tclient.mode == "login0":
		tclient.send("login:")
	elif tclient.mode == "login1":
		tclient.send("password:")
		

