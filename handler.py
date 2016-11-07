import login
import game

client_modes = {}

# login modes
client_modes.update( {"login0":login.loginMenu}) # reget login
client_modes.update( {"login1":login.loginMenu}) # get password
client_modes.update( {"login2":login.loginMenu}) # login auth
client_modes.update( {"loginnew":login.loginMenu}) # new login query
client_modes.update( {"loginnewpass":login.loginMenu}) # new login pass verify
client_modes.update( {"loginnewpass2":login.loginMenu}) # new login pass verify


# main modes
client_modes.update( {"maingame":game.mainGame}) # main game prompt

def handleClient(tclient):
	
	cc = tclient.last_input
	
	# run loop, skipping input if set
	while tclient.skip_input >= 0:
	
		# client output, goto client mode function pointer
		client_modes[ tclient.mode ](tclient)
		
		# client input
		if cc == "quit":
			tclient.disconnect()
		
		# decrement input skip for next pass
		if tclient.skip_input != 0:
			tclient.last_input = ""
		tclient.skip_input -= 1
	
	# reset input skip counter
	tclient.skip_input = 0

