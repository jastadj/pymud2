from tools import *

import defs

# class refs
ROOM = None
COMMAND = None
COMMAND_SET = None

# objects
server = None
rooms = None
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
                    tclient.send("Unrecognized command!\n")
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

def getCurrentRoomNum(tuser):
    for room in range(0, len(rooms) ):
        if tuser.current_room == room:
            return room
    return None

def getCurrentRoom(tuser):
    for room in range(0, len(rooms) ):
        if tuser.current_room == room:
            return rooms[room]
    return None

def showHelpMenu(tuser, cdict):
    
    tset = None
    
    try:
        tset = cdict["source"]
    except:
        tuser.send("Unable to print help menu, no source in dictionary!")
        return
    
    tuser.send("%sHelp Menu%s\n" % (setColor(COLOR_MAGENTA, True), resetColor() ) )
    tuser.send("%s---------%s\n" % ( setColor(COLOR_MAGENTA, False) , resetColor() ) )
    tuser.send("%s" % setColor(COLOR_GREEN) )
    for i in range(0, tset.count() ) :
        tuser.send("%s - %s\n" %(tset.commands[i].cdict["name"], tset.commands[i].cdict["helpstring"]) )
    tuser.send("%s" % resetColor() )

def doLook(tuser, cdict, *argv):
    args = []
    if argv[0] == None:
        print "look - no arguments"
        args = None
    else:
        print "look - arguments"
        for a in argv[0]:
            args.append(a)

    if args:
        print "doing item or other look"
    else:
        print "Doing room look"
        doLookRoom(tuser, getCurrentRoom(tuser) )       
        

def doLookRoom(tuser, troom):
    if troom == None:
        tuser.send("Invalid room look - room is null!\n")
        return

    tuser.send("%s%s%s\n\n" %(setColor(COLOR_CYAN, True), troom.name, resetColor()) )
    tuser.send("%s\n" %troom.desc)

def doMove(tuser, cdict):
	tdir = cdict["dir"]
	
	oroom = getCurrentRoom(tuser)
	
	if oroom == None:
		tuser.send("Error getting origin room, null!\n")
		return
		
	if tdir < 0 or tdir >= len(rooms):
		tuser.send("Error moving, target room id#%dout of bounds!\n" %tdir)
		return
	
	if oroom.exits[tdir] == None:
		tuser.send("No exit in that direction!\n")
		return
	
	tuser.current_room = tdir
	
def doDebug(tuser, cdict):
	troom = getCurrentRoom(tuser)
	troom.show()

if __name__ == "__main__":
    
    import testuser
    import command
    import room
    global rooms  
    
    rooms = []
    rooms.append(room.Room())
    
    cmds_main = command.initMainCommands()
    
    tuser = testuser.TestUser()
    tuser.send("Test\n")

    doquit = False

    doLookRoom(tuser, rooms[0])

    tuser.send(">")
    
    while not doquit:

        

        tuser.last_input = raw_input()

        if tuser.last_input == "quit":
            doquit = True

        mainGame(tuser)
    
    
