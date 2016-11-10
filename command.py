import game
from tools import *

def commandError(tuser, cdict):
    tuser.send("Unrecognized command!\n")

class Command(object):
    def __init__(self, name, helpstr, fptr, hasargs = False):
        self.cdict = {"name":name,
                      "helpstring":helpstr,
                      "hasargs":False,
                      "function":fptr}
        if hasargs:
            self.cdict.update({"hasargs":True})
        
    def getFunction(self):
        return self.cdict["function"]

    def execute(self, tuser, *argv):
        if self.cdict["function"] == None:
            pass
        elif not self.cdict["hasargs"]:
            self.cdict["function"](tuser, self.cdict)
        else:
            args = []
            if len(argv[0]) == 0:
               args.append("")
               args = None
            else:
                for a in argv[0]:
                    args.append(a)
            self.cdict["function"](tuser, self.cdict, args)

class CommandSet(object):

    invalidcmd = Command("invalidcmd", "invalidcmd", commandError)
    
    def __init__(self):
        self.commands = []
        self.aliases = {}
    
    def add(self, name, helpstr, fptr, hasargs = False):
        self.commands.append( Command(name, helpstr, fptr, hasargs) )

    def count(self):        
        return len(self.commands)
    
    def getAndExecute(self, tuser, cstr, *argv):
		tcmds = self.getCommand(cstr)
		tcmds[0].execute(tuser, argv)
    
    def getCommand(self, cstr):
        foundcmds = []
        
        # if command string is an alias
        if cstr in self.aliases.keys():
            cstr = self.aliases[cstr]
        
        for i in range(0, self.count() ):
            #found absolute
            if self.commands[i].cdict["name"] == cstr:
                return [self.commands[i]]
            #found partial match
            elif self.commands[i].cdict["name"].startswith(cstr):
                foundcmds.append(self.commands[i])
        if len(foundcmds) == 0:
            return [self.invalidcmd]
        else:
            return foundcmds
           

def initMainCommands():
    cs = CommandSet()
    cs.add("help", "Show help menu", showHelpMenu)
    cs.commands[-1].cdict.update({"source":cs})
    
    cs.add("look", "Look at something", doLook, True)
    cs.add("north", "Move north", doMove)
    cs.commands[-1].cdict.update({"dir":0})
    cs.add("south", "Move south", doMove)
    cs.commands[-1].cdict.update({"dir":1})
    cs.add("east", "Move east", doMove)
    cs.commands[-1].cdict.update({"dir":2})
    cs.add("west", "Move west", doMove)
    cs.commands[-1].cdict.update({"dir":3})
    
    #cs.add("debug", "do something", doDebug)
    
    
    # setup command aliases
    cs.aliases.update( {"?":"help"})
    
    return cs

#####################################################################
##      COMMANDS



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
        doLookRoom(tuser, getCurrentRoom(tuser))       
        

def doLookRoom(tuser, troom):
    if troom == None:
        tuser.send("Invalid room look - room is null!\n")
        return

    tuser.send("%s%s%s\n\n" %(setColor(COLOR_CYAN, True), troom.name, resetColor()) )
    tuser.send("%s\n" %troom.desc)

def doMove(tuser, cdict):
    tdir = cdict["dir"]
    
    tuser.send("tdir=%d\n" %tdir)
    
    oroom = getCurrentRoom(tuser)
    
    if oroom == None:
        tuser.send("Error getting origin room, null!\n")
        return
        
    if tdir < 0 or tdir >= len(getCurrentZone().rooms):
        tuser.send("Error moving, target room id#%dout of bounds!\n" %tdir)
        return
    
    if oroom.exits[tdir] == None:
        tuser.send("No exit in that direction!\n")
        return
    
    tuser.current_room = tdir
    

def getCurrentRoomNum(tuser):
    pass

def getCurrentRoom(tuser):
    pass

def getCurrentZone(tuser):
    pass


#####################################################################
if __name__ == "__main__":
    import testuser
    
    tuser = testuser.TestUser()
    
    doquit = False
    
    def t(tuser, cdict):
        tuser.send("This is a test function!\n")
    
    def ta(tuser, cdict, *argv):
        tuser.send("This is a test function with args!\n")
        if argv[0] == None:
            print "No args"
        else:
            for a in argv[0]:
                print a
    
    def quittest(tuser, cdict):
        global doquit
        doquit = True
    
    def dohelp(tuser, cdict):
        print "Help Menu"
        print "---------"
        for i in cset.commands:
            print "%s - %s" %(i.cdict["name"], i.cdict["helpstring"])
    
    cset = CommandSet()
    cset.add("t", "Tests a function with no args", t)
    cset.add("ta", "Tests a function with args", ta, True)
    cset.add("help", "Help menu", dohelp)
    cset.add("quit", "Quit test", quittest)
    
    cset.aliases.update( {"?":"help"} )
    
    while not doquit:
        
        tuser.send(">")
        tuser.last_input = raw_input()
        
        cmds = tuser.last_input.split()
        
        
        # if no commands were entered, ignore
        if len(cmds) == 0:
            continue
         
        # get commands from input
        tcmd = cset.getCommand(cmds[0])
        
        # if no valid command was found
        if tcmd == None:
            tuser.send("Invalid command!\n")
        # if only one command was found, execute
        elif len(tcmd) == 1:
            tcmd[0].execute(tuser,cmds[1:])
        # or if multiple commands found, print them
        else:
            for c in tcmd:
                print a.cdict["name"]
        
        
        
