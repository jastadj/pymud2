import defs

# class refs
ROOM = None
ZONE = None
ITEM = None
COMMAND = None
COMMAND_SET = None
CHARACTER = None

# objects
server = None
credentials = None
zones = None
cmds_main = None
clients = None
items = None
items_common = None

# function refs
processnoncmd = None

# main
def mainGame(tuser):
    
    do_passes = 0
    
    while do_passes >= 0:
        
        if tuser.mode == "maingame":
            
            cmds = tuser.last_input.split()
            
            if len(cmds) > 0:
                
                # process main game command
                tcmd = cmds_main.getCommand(cmds[0])
                
                # no valid command found
                if tcmd == None:
					if not processnoncmd(tuser, tuser.getLastInput()):
						tuser.send("Invalid command!\n")
                # exactly one command found, execute
                elif len(tcmd) == 1:
                    tcmd[0].execute(tuser, cmds[1:])
                # multiple commands found, print them
                else:
                    for c in tcmd:
                        tuser.send("%s\n" %c)
            
            tuser.send(">")
            
            
        # if entering the game after login
        elif tuser.mode == "maingamestart":
            cmds_main.getAndExecute(tuser, "look")
            tuser.mode = "maingame"
            do_passes = 1
        
        do_passes -= 1

  
    
