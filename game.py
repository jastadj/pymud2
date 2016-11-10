import defs

# class refs
ROOM = None
ZONE = None
COMMAND = None
COMMAND_SET = None

# objects
server = None
zones = None
cmds_main = None
clients = None

# main
def mainGame(tclient):
    
    do_passes = 0
    
    while do_passes >= 0:
        
        if tclient.mode == "maingame":
            
            cmds = tclient.last_input.split()
            
            if len(cmds) > 0:
                # process main game command
                tcmd = cmds_main.getCommand(cmds[0])
                
                # no vaild command found
                if tcmd == None:
                    tclient.send("ERROR!\n")
                # exactly one command found, execute
                elif len(tcmd) == 1:
                    tcmd[0].execute(tclient, cmds[1:])
                # multiple commands found, print them
                else:
                    for c in tcmd:
                        tclient.send("%s\n" %c)
            
            tclient.send(">")
            
            
        # if entering the game after login
        elif tclient.mode == "maingamestart":
            #tcmd = command.getCommand("look")
            #tcmd.execute(tclient)
            tclient.mode = "maingame"
            do_passes = 1
        
        do_passes -= 1





if __name__ == "__main__":
    
    import testuser
    import command
    import room
    
    rooms = []
    rooms.append(room.Room())
    
    cmds_main = command.initMainCommands()
    
    tuser = testuser.TestUser()
    tuser.send("Test\n")

    doquit = False


    cmds_main.getAndExecute(tuser, "look")

    tuser.send(">")
    
    while not doquit:

        

        tuser.last_input = raw_input()

        if tuser.last_input == "quit":
            doquit = True

        mainGame(tuser)
    
    
