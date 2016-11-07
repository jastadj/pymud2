from tools import *
import room

commands = []


class command(object):
    def __init__(self, name, helpstr, fptr, hasargs = False):
        self.name = name
        self.helpstr = helpstr
        self.__fptr = fptr
        self.hasargs = hasargs
    def execute(self, tuser, *argv):
        if self.__fptr == None:
            pass
        elif not self.hasargs:
            self.__fptr(tuser)
        else:
			# arguments provided
            if len(argv) > 0:
                self.__fptr(tuser, argv[0])
            else:
                self.__fptr(tuser, [""])

def getCommand(cstr):
    for i in range(0, len(commands)):
        if commands[i].name == cstr:
            return commands[i]
    return None
    
def showHelp(tuser):
    tuser.send("%sHelp Menu%s\n" % (setColor(COLOR_MAGENTA, True), resetColor() ) )
    tuser.send("%s---------%s\n" % ( setColor(COLOR_MAGENTA, False) , resetColor() ) )
    tuser.send("%s" % setColor(COLOR_GREEN) )
    for i in range(0, len(commands) ) :
        tuser.send("%s - %s\n" %(commands[i].name, commands[i].helpstr) )
    tuser.send("%s" % resetColor() )

def doLook(tclient):
	room.doLookRoom(tclient)

commands.append( command("help", "Show help menu", showHelp) )
commands.append( command("look", "Look at your surroundings", doLook) )
