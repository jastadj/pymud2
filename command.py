import game
from tools import *
import copy
import defs

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

    def __init__(self):
        self.commands = []
        self.aliases = {}
        self.invalidFunction = None
        
    def add(self, name, helpstr, fptr, hasargs = False):
        self.commands.append( Command(name, helpstr, fptr, hasargs) )

    def setInvalidFunction(self, func):
        self.invalidFunction = func
        
    def count(self):
        return len(self.commands)

    def getAndExecute(self, tuser, cstr, *argv):
        tcmds = self.getCommand(cstr)
        tcmds[0].execute(tuser, argv)
    
    def getInvalidFunction(self):
        return self.invalidFunction
    
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
            return None
        else:
            return foundcmds


def initMainCommands():
    cs = CommandSet()
    cs.add("help", "Show help menu", showHelpMenu)
    cs.commands[-1].cdict.update({"source":cs})
    cs.add("look", "Look at something", doLook, True)
    cs.add("say", "Say something", doSay, True)
    cs.add("inventory", "Show inventory", doShowInventory)
    cs.add("get","Get something", doGet, True)
    cs.add("drop","Drop something", doDrop, True)
    
    
    #cs.add("debug", "do something", doDebug)


    # setup command aliases
    cs.aliases.update( {"?":"help"})
    cs.aliases.update( {"s":"south"} )

    return cs

def mainGameInvalid(tuser):
    
    cstr = tuser.getLastInput()
    
    # check to see if noncmd is actually an exit
    troom = getCurrentRoom(tuser)
    
    if troom.isExit(cstr):
        doMove(tuser, troom.getExit(cstr) )
        return True
    
    return False
    
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
    # no arguments, do a room look
    if argv[0] == None:
        doLookCurrentRoom(tuser)
        return
    # arguments
    else:
        for a in argv[0]:
            args.append(a)

    # get a string from args
    monoarg = " ".join(args)

    # current room
    troom = getCurrentRoom(tuser)
    if troom == None:
        print "ERROR do look, current room NULL!"
        return

    # check descriptors
    if monoarg in troom.descriptors.keys():
        tuser.send("%s\n" %troom.descriptors[monoarg])
        return

    titems = None
    
    # check items in room
    titems = findItemsInList(monoarg, troom.getItems())
    if titems != None:
        tuser.send("%s\n" %titems[0].getDesc() )
        return

    # check items in inventory
    titems = findItemsInList(monoarg, tuser.char.getInventory())
    if titems != None:
        tuser.send("%s\n" %titems[0].getDesc())
        return
  
    # check mobs in room
    tmobs = findMobsInList(monoarg, troom.getMobs())
    if tmobs != None:
        tuser.send("%s\n" %tmobs[0].getDesc())
        return
        
    tuser.send("You do not see that here.\n")


def doLookRoom(tuser, troom):
    if troom == None:
        tuser.send("Invalid room look - room is null!\n")
        return

    tuser.send("%s%s%s\n" %(setColor(COLOR_CYAN, True), troom.name, resetColor()) )
    desclines = fitStringToWidth(troom.desc)
    for l in desclines:
        tuser.send("%s\n" %l)

    # get room exits
    estring = "Exits: "
    for e in troom.exits:
        if e == troom.exits[-1]:
            estring += e.getName()
        else:
            estring += e.getName() + ", "
    # if there are no room exits
    if len(troom.exits) == 0:
        estring = "There are no obvious exits."
    
    tuser.send("%s\n" %estring)
    
        
    # list items here
    ilist = troom.getItems()
    for i in ilist:
        tuser.send("    %s %s\n" %(i.getArticle(), i.getDescName()) )
        
    # list players and mobs here
    charlist = []
    charlist += troom.getMobs()
    for m in charlist:
        tuser.send("%s is here.\n" %m.getName())

def doLookCurrentRoom(tuser):
    
    croom = getCurrentRoom(tuser)

    # debug
    print "DEBUG:"
    croom.show()    
    
    doLookRoom(tuser, croom)

def actorMove(tactor, rexit):
    
    # set actors current room to exit's room number
    tactor.setCurrentRoom( rexit.getRoomNum() )
    
    # if exit's zone number is specified, set actors zone number
    if rexit.getZoneNum() != None:
        tactor.setCurrentZone( rexit.getZoneNum() )

def doMove(tuser, rexit):
    
    # move user's character
    actorMove(tuser.char, rexit)
    
    # by default, do a look room command for player
    doLookCurrentRoom(tuser)

def actorSay(tactor, saystr):
    pass
    
def doSay(tuser, cdict, *argv):
    args = []
    if argv[0] == None:
        args = None
    else:
        for a in argv[0]:
            args.append(a)

    if args:

        # get current room
        troom = getCurrentRoom(tuser)

        # get all players in room
        ulist = troom.getAllClients()


        # all arguments = say string
        saystr = " ".join(args)

        tuser.send("You say \"%s\"\n" %saystr)

        broadcastToRoomEx(tuser, "%s says \"%s\"\n" %(tuser.char.getName(), saystr) )

    else:
        tuser.send("Say what?\n")

def broadcastToRoomEx(tuser, tmsg):
    
    troom = getCurrentRoom(tuser)
    
    ulist = troom.getAllClients()
    
    ulist.remove(tuser)
    
    for u in ulist:
        u.send("%s" %tmsg)


def getCurrentRoom(tuser):

    crnum = tuser.char.getCurrentRoom()
    tz = getCurrentZone(tuser)
    tr = None

    try:
        tr = tz.rooms[crnum]
    except:
        print "Error getting current player room @ room #%d!!" %crnum
        return None

    return tr

def getCurrentZone(tuser):

    tz = None
    pzi = tuser.char.getCurrentZone()

    try:
        tz = game.zones[pzi]
    except:
        print "Error getting current zone, index %d out of range!" %pzi
        return None

    return tz

def getNewItem(idesc):
    
    titem = findItemInList(idesc, game.items)
    
    if titem != None:
        return copy.copy(titem)
    else:
        return None

def findItemInList(idesc, ilist):
    ids = idesc.split()
    
    iname = ids[-1]
    
    foundlist = []
    
    for i in ilist:
        if i.getName() == iname:
            foundlist.append(i)
    
    if len(foundlist) == 0:
        #print "Could not find item with \"%s\"" %idesc
        return None
    
    elif len(foundlist) > 1:
        print "Multiple items of this name found:"
        for i in foundlist:
            print i.getName()
        #NOT IMPLEMENTED YET, NEED TO CHECK OTHER IDS
        return None
    else:
        #print "found item:%s" %foundlist[0].getName()
        return foundlist[0]

def findItemsInList(idesc, ilist):
    ids = idesc.split()
    
    iname = ids[-1]
    
    foundlist = []
    
    for i in ilist:
        if i.getName() == iname:
            foundlist.append(i)
    
    if len(foundlist) == 0:
        #print "Could not find item with \"%s\"" %idesc
        return None
    
    else:
        return foundlist

def doShowInventory(tuser, cdict):
    tuser.send("You are carring:\n")
    tuser.send("----------------\n")
    
    titems = tuser.char.getInventory()
    if len(titems) == 0:
        tuser.send("    Nothing!\n")
    else:
        for i in titems:
            tuser.send("    %s %s\n" %(i.getArticle(),i.getDescName()) )

def actorGet(tactor, getstr):
    pass

def doGet(tuser, cdict, *argv):
    args = []
    # no arguments, do a room look
    if argv[0] == None:
        tuser.send("Get what?\n")
        return
    # arguments
    else:
        for a in argv[0]:
            args.append(a)

    # get a string from args
    monoarg = " ".join(args)

    # current room
    troom = getCurrentRoom(tuser)
    if troom == None:
        print "ERROR do look, current room NULL!"
        return

    ritems = troom.getItems()

    # look for item
    titems = findItemsInList(monoarg, ritems)
    
    if titems == None:
        tuser.send("You do not see that here.\n")
    # item found, get it and add to player inventory, remove from list
    else:
        troom.removeItem(titems[0])
        tuser.char.addItem(titems[0])
        tuser.send("You take the %s.\n" %titems[0].getDescName() )
        
        broadcastToRoomEx(tuser, "%s takes a %s.\n" %(tuser.char.getName(), titems[0].getDescName()) )
        
def actorDrop(tactor, dropstr):
    pass

def doDrop(tuser, cdict, *argv):
    args = []
    # no arguments, do a room look
    if argv[0] == None:
        tuser.send("Drop what?\n")
        return False
    # arguments
    else:
        for a in argv[0]:
            args.append(a)

    # get a string from args
    monoarg = " ".join(args)

    # current room
    troom = getCurrentRoom(tuser)
    if troom == None:
        print "ERROR do look, current room NULL!"
        return False

    pitems = tuser.char.getInventory()

    #look for item
    titems = findItemsInList(monoarg, pitems)
    
    
    if titems == None:
        tuser.send("You are not carrying that!\n")
    # item found, get it and add to player inventory, remove from list
    else:
        if not tuser.char.removeItem(titems[0]):
            print "Error removing item, not on character!"
            return False
        troom.addItem(titems[0])
        tuser.send("You drop the %s.\n" %titems[0].getName() )

        broadcastToRoomEx(tuser, "%s drops a a %s.\n" %(tuser.char.getName(), titems[0].getDescName()) )
        
        return True

def getNewMob(mdesc):
    
    tmob = findMobInList(mdesc, game.mobs)
    
    if tmob != None:
        return copy.copy(tmob)
    else:
        return None

def findMobsInList(mdesc, mlist):
    
    ids = mdesc.split()
    
    mname = ids[-1]
    
    foundlist = []
    
    for m in mlist:
        if m.getName() == mname:
            foundlist.append(m)
    
    if len(foundlist) == 0:
        #print "Could not find mob with \"%s\"" %mdesc
        return None
    
    else:
        return foundlist

def findMobInList(mdesc, mlist):
    
    ids = mdesc.split()
    
    mname = ids[-1]
    
    foundlist = []
    
    for m in mlist:
        if m.getName() == mname:
            foundlist.append(m)
    
    if len(foundlist) == 0:
        #print "Could not find mob with \"%s\"" %mdesc
        return None
    
    elif len(foundlist) > 1:
        print "Multiple mobs of this name found:"
        for m in foundlist:
            print m.getName()
        #NOT IMPLEMENTED YET, NEED TO CHECK OTHER IDS
        return None
    else:
        #print "found mob:%s" %foundlist[0].getName()
        return foundlist[0]

#####################################################################
if __name__ == "__main__":
    import testclient
    import zone
    import room
    import item
    import character

    # init test mode
    defs.configTestMode()

    # init user
    tuser = testclient.TestClient()
    tuser.char = character.Character()
    game.clients = [tuser]
    
    doquit = False
    
    
    # init items
    item.loadItems()
    
    # init zones
    game.zones = []
    newzone = zone.Zone()

    
    # build test rooms
    newroom = room.Room()
    newroom.name = "Bathroom"
    newroom.desc = ["You are standing in a cramped dingy bathroom that smells of ",
                    "old urine.  The yellow stained walls are streaked with water ",
                    "damage. A sink hangs precariously from the wall."]
    newroom.desc = "".join(newroom.desc)
    newroom.descriptors.update( {"sink":"The sink is layed with years of soap scum."})
    newroom.addNewItem("sword")
    newroom.inventory[-1].properties.update( {"desc":"A plain long sword."})
    newroom.addExit("north", 1)
    
    newzone.addRoom(newroom)
    newroom = room.Room()
    newroom.name = "Bedroom"
    newroom.desc = "This bedroom makes you uncomfortable."
    newroom.addExit("south",0)
    newzone.addRoom(newroom)
    game.zones.append(newzone)
    
    
    
    newzone2 = zone.Zone()
    newroom = room.Room()
    newroom.name = "Outside"
    newroom.desc = "It's beautiful out here!"
    newzone2.addRoom(newroom)
    game.zones.append(newzone2)
    
    zone.saveZones()
    
    for z in game.zones:
        z.show()


    """
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
    """

    cset = initMainCommands()


    def showSelf(tuser, cdict):
        tuser.show()
        
    def showRoom(tuser, cdict):
        getCurrentRoom(tuser).show()
    
    def showZone(tuser, cdict):
        getCurrentZone(tuser).show()


    cset.add("showself", "Client debug", showSelf)
    cset.add("showroom", "Room debug", showRoom)
    cset.add("showzone", "Zone debug", showZone)

    # test
    tuser.current_zone = 0



    cset.getAndExecute(tuser, "look")

    while not doquit:

        tuser.send(">")
        tuser.last_input = raw_input()

        cmds = tuser.last_input.split()

        # if no commands were entered, ignore
        if len(cmds) == 0:
            continue

        if cmds[0] == "quit":
            doquit = True
            continue

        # get commands from input
        tcmd = cset.getCommand(cmds[0])

        # if no valid command was found
        if tcmd == None:
            tuser.send("ERROR\n")
        # if only one command was found, execute
        elif len(tcmd) == 1:
            tcmd[0].execute(tuser,cmds[1:])
        # or if multiple commands found, print them
        else:
            for c in tcmd:
                print c.cdict["name"]



