import defs

# class refs
COMMAND = None
COMMAND_SET = None

# see gameinit - initializes object classes in dict
OBJECT_CLASSES = {}

# objects(lists)
server = None
timer = None
credentials = None
cmds_main = None
clients = None

def lobby(tuser):
    
    do_passes = 0
    
    while do_passes >= 0:
        
        if tuser.mode == "lobby":
            
            cmds = tuser.getlastinput().split()
            
            if len(cmds) > 0:
                pass
            
            tuser.send("echo:%s\n" %tuser.getlastinput())
            tuser.send(">")
        
        do_passes -= 1 

# main
def maingame(tuser):
    
    do_passes = 0
    
    while do_passes >= 0:
        
        if tuser.mode == "maingame":
            
            cmds = tuser.getlastinput().split()
            
            if len(cmds) > 0:
                
                # process main game command
                tcmd = cmds_main.getcommand(cmds[0])
                
                # no valid command found
                if tcmd == None:
					cmds_main.getinvalidfunction()(tuser)
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
            cmds_main.getandexecute(tuser, "look")
            tuser.mode = "maingame"
            do_passes = 1
        
        do_passes -= 1

  
    
