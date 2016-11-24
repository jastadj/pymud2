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
    
    def setalias( self, aliasdict ):
        self.aliases.update( aliasdict)
    
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
    cd.add("inventory", "Show inventory", doinventory, False)
    cd.add("get", "Get an item", dogetitem, True)
    cd.add("drop", "Drop an item", dodropitem, True)
    
    cd.add("debug", "Do a debug #", dodebug, True)
    cd.add("showuid", "Show object of uid#", dodebugshowuid, True)
    cd.add("showiid", "Show object instance of iid#", dodebugshowiid, True)
    
    # set aliases
    cd.setalias( {"i":"inventory"} )

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
##      DEBUG
def dodebug(tuser, cdict, *argv):
    args = []
    # no arguments, do a room look
    if argv[0] == None:
        pass
    # arguments
    else:
        for a in argv[0]:
            args.append(a)
    
    debugmode = 0
    
    if len(args) == 1:
        try:
            debugmode = int(args[0])
        except:
            debugmode = 0
    
    if debugmode == 0:
        for o in hub.worldobjects.keys():
            tuser.send("%d : %s (%s)\n" %(o, hub.worldobjects[o].getnameex(), hub.worldobjects[o].gettype() ) )
        
        try:
            tempval = hub.worldobjects.keys()[0]
            uidcounter = hub.worldobjects[tempval].uidcount
            tuser.send("uidcounter = %d\n" %uidcounter )
        except:
            pass
        
        tuser.send("%d world objects.\n" %len(hub.worldobjects.keys() ) )
    
    if debugmode == 1:
        for o in hub.worldobjects_instance.keys():
            tuser.send("%d : %s (%s)\n" %(o, hub.worldobjects_instance[o].getrefname(), hub.worldobjects_instance[o].gettype() ) )
        
        try:
            tempval = hub.worldobjects_instance.keys()[0]
            iidcounter = hub.worldobjects_instance[tempval].iidcount
            tuser.send("iidcounter = %d\n" %iidcounter)
        except:
            pass
        
        tuser.send("%d world instance objects.\n" %len(hub.worldobjects_instance.keys() ) )            


def dodebugshowuid(tuser, cdict, *argv):
    args = []
    # no arguments, do a room look
    if argv[0] == None:
        pass
    # arguments
    else:
        for a in argv[0]:
            args.append(a)
    
    if len(args) == 0:
        return
        
    tgtuid = None
    
    try:
        tgtuid = int(args[0])
        hub.worldobjects[tgtuid].show()
    except:
        return

def dodebugshowiid(tuser, cdict, *argv):
    args = []
    # no arguments, do a room look
    if argv[0] == None:
        pass
    # arguments
    else:
        for a in argv[0]:
            args.append(a)
    
    if len(args) == 0:
        return
        
    tgtiid = None
    
    try:
        tgtiid = int(args[0])
        hub.worldobjects_instance[tgtiid].show()
    except:
        return

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

def doroombroadcast(troom, thirdpersonmsg, tuser = None, firstpersonmsg = None):
    
    clist = getallclientsinroom(troom)
    
    if tuser != None:
        if firstpersonmsg != None:
            tuser.send(firstpersonmsg)
        else:
            tuser.send(thirdpersonmsg)
    
    for c in clist:
        
        if c != tuser:
            c.send(thirdpersonmsg)
    

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
    
    doroombroadcast(getcurrentroom(tuser), cmsg, tuser, umsg)


###########################################
##      CHARACTER



###########################################
##      ITEMS

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
        return
    
    
    # remove junk words
    if "at" in args:
        args.remove("at")
    
    monoarg = " ".join(args)
    
    descstr = None
    troom = getcurrentroom(tuser)
    
    # check if item in inventory
    for i in tuser.char.getinventory():
        if i.getref().hasmatch(monoarg):
            descstr = i.getref().getdescription()
            break
    
    # check if item in room
    if descstr == None:
        for i in troom.getitems():
            if i.getref().hasmatch(monoarg):
                descstr = i.getref().getdescription()
                break
    
    # check if player is looking at mob
    if descstr == None:
        for m in troom.getmobs():
            if m.getref().hasmatch(monoarg):
                descstr = m.getref().getdescription()
    
    # check room descriptors
    if descstr == None:
        if monoarg in troom.getdescriptors():
            descstr = troom.getdescriptors()[monoarg]
    
    if descstr != None:
        
        tuser.send("%s\n" %descstr )
        return
    else:
        tuser.send("You do not see that here!\n")
        return
        
    

def doinventory(tuser, cdict):
    
    tinv = tuser.char.getinventory()
    
    tuser.send("Inventory:\n")
    tuser.send("----------\n")
    
    if len(tinv) == 0:
        tuser.send("  You are not carrying anything!\n")
    else:
        for i in tinv:
            tuser.send("  %s\n" %i.getrefname() )

def dogetitem(tuser, cdict, *argv):
    args = []
    # no arguments, do a room look
    if argv[0] == None:
        pass
    # arguments
    else:
        for a in argv[0]:
            args.append(a)
    
    if len(args) == 0:
        tuser.send("Get what?\n")
        return False
        
    monoargs = " ".join(args)    
    
    # get current room
    troom = getcurrentroom(tuser)
    
    titem = None
    
    # look for target item in room item list
    for i in troom.getitems():
        if i.getref().hasmatch(monoargs):
            
            # get item
            titem = i
            
            # remove item from room
            troom.removeitem(titem)
            
            # add item to player
            tuser.char.additem(titem)
            
            tmsg = "%s picks up %s.\n" %(tuser.char.getnameex(), titem.getref().getnameex() )
            umsg = "You pick up %s.\n" %titem.getref().getnameex()
            
            doroombroadcast(troom, tmsg, tuser, umsg)
            
            return True

    # target item was not found anywhere
    if titem == None:
        tuser.send("You do not see that here!\n")
        return False
    
def dodropitem(tuser, cdict, *argv):
    args = []
    # no arguments, do a room look
    if argv[0] == None:
        pass
    # arguments
    else:
        for a in argv[0]:
            args.append(a)
    
    if len(args) == 0:
        tuser.send("Drop what?\n")
        return False
        
    monoargs = " ".join(args)    
    
    # get current room
    troom = getcurrentroom(tuser)
    
    titem = None
    
    # look for target item in player inventory
    for i in tuser.char.getinventory():
        if i.getref().hasmatch(monoargs):
            
            # get item
            titem = i
            
            # remove item from player inventory
            tuser.char.removeitem(titem)
            
            # add item to room
            troom.additem(titem)
            
            tmsg = "%s drops %s.\n" %(tuser.char.getnameex(), titem.getref().getnameex())
            umsg = "You drop %s.\n" %titem.getref().getnameex()
            doroombroadcast(troom, tmsg, tuser, umsg)
            
            return True

    # target item was not found anywhere
    if titem == None:
        tuser.send("You do not have that!\n")
        return False    

def newitem(uid):
    newitem = hub.ITEM(uid)
    return newitem


###########################################
##      ROOM

def getcurrentroom(tuser):
    tzone = tuser.char.getcurrentzoneid()
    
    troom = hub.zones[tzone].getroom(tuser.char.getcurrentroomid())
    
    return troom    

def getallclientsinroom(troom):
    
    clist = []
    
    for c in hub.clients:
        if c.char.getcurrentroomid() == troom.getroomid():
            if c.char.getcurrentzoneid() == troom.getzoneid():
                clist.append(c)
    
    return clist

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
    
    for m in troom.getmobs():
        tuser.send("    %s\n" %m.getrefname() )
    
    for i in troom.getitems():
        tuser.send("    %s\n" %i.getrefname() )
        
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



