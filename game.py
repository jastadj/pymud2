
# class refs
ROOM = None
COMMAND = None

# objects
server = None
rooms = None
commands = None


# main
def mainGame(tclient):
	
	do_passes = 0
	
	while do_passes >= 0:
		
		if tclient.mode == "maingame":
			
			cmds = tclient.last_input.split()
			
			if len(cmds) > 0:
				# process main game command
				tcmd = getCommand(cmds[0])
				
				if tcmd != None:
					tcmd.execute(tclient)
				else:
					tclient.send("Command not recognized!\n")
			
			tclient.send(">")
			
		# if entering the game after login
		elif tclient.mode == "maingamestart":
			#tcmd = command.getCommand("look")
			#tcmd.execute(tclient)
			tclient.mode = "maingame"
			do_passes = 1
		
		do_passes -= 1

def getCommand(cmdlist, cstr):
    for i in range(0, len(cmdlist)):
        if cmdlist[i].name == cstr:
            return cmdlist[i]
    return None

def showHelp(cmdlist, tuser):
    tuser.send("%sHelp Menu%s\n" % (setColor(COLOR_MAGENTA, True), resetColor() ) )
    tuser.send("%s---------%s\n" % ( setColor(COLOR_MAGENTA, False) , resetColor() ) )
    tuser.send("%s" % setColor(COLOR_GREEN) )
    for i in range(0, len(cmdlist) ) :
        tuser.send("%s - %s\n" %(cmdlist[i].name, cmdlist[i].helpstr) )
    tuser.send("%s" % resetColor() )

