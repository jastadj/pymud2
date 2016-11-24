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
        tcmds = self.getcommand(cstr)
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
    cd = commandset()
    cd.add("help", "Show help menu", showhelpmenu)
    cd.commands[-1].cdict.update({"source":cd})
    cd.add("color", "Color on or off", docolor, True)
    cd.add("look", "Look at something", dolook, True)
    cd.add("say" , "Say something", dosay, True)

    return cd

def maingameinvalid(tuser):
    
    # auto alias common directions
    i = tuser.getlastinput()
    
    if i == "n": i = "north"
    elif i == "s": i = "south"
    elif i == "e": i = "east"
    elif i == "w": i = "west"
    
    # check to see if command was an exit
    troom = getcurrentroom(tuser)
    if i in troom.getexits().keys():
        doroomexit(tuser, i)
        return
    
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
        pass
    # arguments
    else:
        for a in argv[0]:
            args.append(a)
    
    
    if len(args) == 0:
        tuser.send("Colors = %s\n" %tuser.account.colors())
        return
    
    if args[0].lower() == "on":
        tuser.account.setcolors(True)
        tuser.send("Colors set to #c6on#cr.\n")
    elif args[0].lower() == "off":
        tuser.account.setcolors(False)
        tuser.send("Colors set to off.\n")
    else:
        tuser.send("Unknown color parameter.  color on or color off.\n")

###########################################
##      COMMUNICATION

def dosay(tuser, cdict, *argv):
    args = []
    # no arguments, do a room look
    if argv[0] == None:
        pass
    # arguments
    else:
        for a in argv[0]:
            args.append(a)
    
    if len(args) == 0:
        tuser.send("Say what?\n")
        return
    
    monoarg = " ".join(args)
    
    cmsg = "%s says \"%s\"\n" %(tuser.char.getname(), monoarg)
    umsg = "You say \"%s\"\n" %(monoarg)
    
    for c in hub.clients:
        if c == tuser:
            tuser.send(umsg)
        else:
            c.send(cmsg)

###########################################
##      ITEMS

def newitem(uid):
    newitem = hub.ITEM(uid)
    return newitem


###########################################
##      ROOM

def getcurrentroom(tuser):
    tzone = tuser.char.getcurrentzoneid()
    
    troom = hub.zones[tzone].getroom(tuser.char.getcurrentroomid())
    
    return troom    

def dolook(tuser, cdict, *argv):
    args = []
    # no arguments, do a room look
    if argv[0] == None:
        pass
    # arguments
    else:
        for a in argv[0]:
            args.append(a)    
    
    # if no arguments provided, look at room
    if len(args) == 0:
        doroomlook(tuser, getcurrentroom(tuser) )

def doroomlook(tuser, troom):
        
    # print room name and desc
    tuser.send("#C6%s#cr\n" %troom.getname() )
    tuser.send("#C0%s#cr\n" %troom.getdescription() )
    
    # print exits
    if len(troom.getexits().keys()) == 0:
        tuser.send("There are no obvious exits.\n")
    else:
        tuser.send("Exits: ")
        
        for e in troom.getexits().keys():
            tuser.send("%s " %e)
        tuser.send("\n")
    
    for i in troom.getinventory():
        tuser.send("    %s\n" %hub.worldobjects[i.getrefuid()].getnameex() )
        
def doroomexit(tuser, exitname):
    
    troom = getcurrentroom(tuser)
    
    # find exit string, and change users room to exit room number
    if exitname in troom.getexits().keys():
        tuser.char.setcurrentroomid( troom.getexits()[exitname])
        doroomlook(tuser, getcurrentroom(tuser) )


#####################################################################
if __name__ == "__main__":
    import hubinit
    hubinit.hubinittest()



