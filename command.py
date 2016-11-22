import hub
from tools import *
import copy
import defs

class command(object):
    def __init__(self, name, helpstr, fptr, hasargs = False):
        self.cdict = {"name":name,
                      "helpstring":helpstr,
                      "hasargs":False,
                      "function":fptr}
        if hasargs:
            self.cdict.update({"hasargs":True})

    def getfunction(self):
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

class commandset(object):

    def __init__(self):
        self.commands = []
        self.aliases = {}
        self.invalidfunction = None
        
    def add(self, name, helpstr, fptr, hasargs = False):
        self.commands.append( command(name, helpstr, fptr, hasargs) )

    def setinvalidfunction(self, func):
        self.invalidfunction = func
        
    def count(self):
        return len(self.commands)

    def getandexecute(self, tuser, cstr, *argv):
        tcmds = self.getCommand(cstr)
        tcmds[0].execute(tuser, argv)
    
    def getinvalidfunction(self):
        return self.invalidfunction
    
    def getcommand(self, cstr):
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
            return None
        else:
            return foundcmds


def initmaincommands():
    cs = commandset()
    cs.add("help", "Show help menu", showhelpmenu)
    cs.commands[-1].cdict.update({"source":cs})
    cs.add("color", "Color on or off", docolor, True)
    

    return cs

def maingameinvalid(tuser):
    
    tuser.send("Invalid command!\n")
    
    return False
    
#####################################################################
##      COMMANDS

def showhelpmenu(tuser, cdict):

    tset = None

    try:
        tset = cdict["source"]
    except:
        tuser.send("Unable to print help menu, no source in dictionary!")
        return

    tuser.send("#C%dHelp Menu\n" % COLOR_MAGENTA )
    tuser.send("#c%d---------\n" % COLOR_MAGENTA )
    tuser.send("#c%d" %COLOR_GREEN )
    for i in range(0, tset.count() ) :
        tuser.send("%s - %s\n" %(tset.commands[i].cdict["name"], tset.commands[i].cdict["helpstring"]) )
    tuser.send("#cr")

def docolor(tuser, cdict, *argv):
    args = []
    # no arguments, do a room look
    if argv[0] == None:
        tuser.send("Colors = %s\n" %tuser.credential.colors)
    # arguments
    else:
        for a in argv[0]:
            args.append(a)
    
    if args[0].lower() == "on":
        tuser.credential.colors = True
        tuser.send("Colors set to #c6on#cr.\n")
    elif args[0].lower() == "off":
        tuser.credential.colors = False
        tuser.send("Colors set to off.\n")
    else:
        tuser.send("Unknown color parameter.  color on or color off.\n")

    

#####################################################################
if __name__ == "__main__":
    import hubinit
    hubinit.hubinittest()



