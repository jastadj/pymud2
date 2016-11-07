import client
import login


client_modes = {}

client_modes.update( {"login0":login.loginMenu})
client_modes.update( {"login1":login.loginMenu})

def handleClient(tclient):
	
	cc = tclient.last_input
	
	# client output
	client_modes[ tclient.mode ](tclient)
	
	# client input
	if cc == "quit":
		tclient.disconnect()
