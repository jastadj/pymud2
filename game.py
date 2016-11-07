import room

import command

def mainGame(tclient):
	
	do_passes = 0
	
	while do_passes >= 0:
		
		if tclient.mode == "maingame":
			
			cmds = tclient.last_input.split()
			
			if len(cmds) > 0:
				# process main game command
				tcmd = command.getCommand(cmds[0])
				
				if tcmd != None:
					tcmd.execute(tclient)
				else:
					tclient.send("Command not recognized!\n")
			
			tclient.send(">")
			
		# if entering the game after login
		elif tclient.mode == "maingamestart":
			tcmd = command.getCommand("look")
			tcmd.execute(tclient)
			tclient.mode = "maingame"
			do_passes = 1
		
		do_passes -= 1

