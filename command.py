import game
from tools import *
import copy
import defs

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
    cs.add("say", "Say something", doSay, True)
    cs.add("inventory", "Show inventory", doShowInventory)
    cs.add("get","Get something", doGet, True)
    cs.add("drop","Drop something", doDrop, True)
    
    
    #cs.add("debug", "do something", doDebug)


    # setup command aliases
    cs.aliases.update( {"?":"help"})
    cs.aliases.update( {"s":"south"} )

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

    
    # check items in room
    for i in troom.getItems():
        if i.descMatches(monoarg):
            tuser.send("%s\n" %i.getDesc())
            return
    
    # check items in inventory
    for i in tuser.char.getItems():
        if i.descMatches(monoarg):
            tuser.csend("%s\n" %i.getDesc())
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
    estrings = []
    for e in range(0, len(defs.DIRECTIONS) ):
        if troom.exits[e] != None:
            estrings.append(defs.DIRECTIONS[e])
    # if room exits were found, build exit string from list
    if len(estrings) != 0:
        eprint = "Exits: "
        for es in estrings:
            if es == estrings[-1]:
                eprint += es
            else:
                eprint += es + ", "
        tuser.send("%s\n" %eprint)
    # or if no exits were found
    else:
        tuser.send("There are no obvious exits.\n")
        
    # list items here
    ilist = troom.getItems()
    for i in ilist:
        tuser.send("    %s %s\n" %(i.getArticle(), i.getDescName()) )
        
    # list players here
    ulist = troom.getAllClients()
    ustr = ""
    ucount = len(ulist)
    for u in ulist:
        if u != tuser:
            if ucount == 2:
                ustr += "%s is here." %u.getName()
            else:
                if u == ulist[-1]:
                    ustr += " and %s is here." %u.getName()
                else:
                    ustr += "%s," %u.getname()
    if ucount > 1:
        tuser.send("%s\n" %ustr)

def doLookCurrentRoom(tuser):
    croom = getCurrentRoom(tuser)
    doLookRoom(tuser, croom)

def doMove(tuser, cdict):
    # get direction value (0=north, 1=south, etc..)
    tdir = cdict["dir"]

    # get room of origin
    oroom = getCurrentRoom(tuser)

    # get zone of origin
    ozone = getCurrentZone(tuser)

    if oroom == None:
        tuser.send("Error getting origin room, null!\n")
        return

    if ozone == None:
        tuser.send("Error getting origin zone, null!\n")
        return

    # get destination room number
    drnum = oroom.exits[tdir]

    # if destination direction has no exit
    if oroom.exits[tdir] == None:
        tuser.send("No exit in that direction!\n")
        return


    # get destination zone number
    dzonenum = tuser.char.getCurrentZone()
    if tdir in oroom.zoneexits:
        dzonenum = oroom.zoneexits[tdir]
    
    # check if destination zone exists
    if dzonenum < 0 or dzonenum >= len(game.zones):
        tuser.send("Error moving, destination zone #%d does not exist!\n" %dzonenum)
        return

    # check if destination room number is within range
    if drnum < 0 or drnum >= len(game.zones[dzonenum].rooms):
        tuser.send("Error moving, target room id#%dout of bounds!\n" %drnum)
        return


    # get destination zone
    dzone = game.zones[dzonenum]

    # get destination room
    droom = dzone.getRoom(drnum)

    # inform players in room of departure
    broadcastToRoomEx(tuser, "%s leaves to the %s.\n" %(tuser.char.getName(), defs.DIRECTIONS[tdir]) )

    # move player to destination room / zone
    tuser.char.setCurrentZone(dzonenum)
    tuser.char.setCurrentRoom(drnum)

    # inform players in room of arrival
    broadcastToRoomEx(tuser, "%s enters from the %s.\n" %(tuser.char.getName(), defs.DIRECTIONS[getOppositeDirection(tdir)]) )

    # automatically do a room look
    doLookCurrentRoom(tuser)



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
        # make copy of item and return
        return foundlist[0]

def doShowInventory(tuser, cdict):
    tuser.send("You are carring:\n")
    tuser.send("----------------\n")
    
    titems = tuser.char.getInventory()
    if len(titems) == 0:
        tuser.send("    Nothing!\n")
    else:
        for i in titems:
            tuser.send("    %s %s\n" %(i.getArticle(),i.getDescName()) )

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
    titem = findItemInList(monoarg, ritems)
    
    if titem == None:
        tuser.send("You do not see that here.\n")
    # item found, get it and add to player inventory, remove from list
    else:
        troom.removeItem(titem)
        tuser.char.addItem(titem)
        tuser.send("You take the %s.\n" %titem.getDescName() )
        
        broadcastToRoomEx(tuser, "%s takes a %s.\n" %(tuser.char.getName(), titem.getDescName()) )
        

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
    titem = findItemInList(monoarg, pitems)
    
    if titem == None:
        tuser.send("You are not carrying that!\n")
    # item found, get it and add to player inventory, remove from list
    else:
        if not tuser.char.removeItem(titem):
			return False
        troom.addItem(titem)
        tuser.send("You drop the %s.\n" %titem.getName() )

        broadcastToRoomEx(tuser, "%s drops a a %s.\n" %(tuser.char.getName(), titem.getDescName()) )
        
        return True

#####################################################################
if __name__ == "__main__":
    import testuser
    import zone
    import room
    import item

    tuser = testuser.TestUser()
    game.clients = [tuser]
    doquit = False
    defs.configTestMode()

    game.zones = []
    newzone = zone.Zone()

    item.loadItems()

    newroom = room.Room()
    newroom.name = "Bathroom"
    newroom.desc = ["You are standing in a cramped dingy bathroom that smells of ",
                    "old urine.  The yellow stained walls are streaked with water ",
                    "damage. A sink hangs precariously from the wall."]
    newroom.desc = "".join(newroom.desc)
    newroom.descriptors.update( {"sink":"The sink is layed with years of soap scum."})
    newroom.exits[0] = 1
    newroom.addNewItem("sword")
    newroom.inventory[-1].properties.update( {"desc":"A plain long sword."})
    
    newzone.addRoom(newroom)
    newroom = room.Room()
    newroom.name = "Bedroom"
    newroom.desc = "This bedroom makes you uncomfortable."
    newzone.addRoom(newroom)
    newroom.exits[1] = 0
    newroom.exits[2] = 0
    newroom.zoneexits.update({2:1})
    game.zones.append(newzone)
    
    
    newzone2 = zone.Zone()
    newroom = room.Room()
    newroom.name = "Outside"
    newroom.desc = "It's beautiful out here!"
    newroom.exits[3] = 1
    newroom.zoneexits.update({3:0})
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
            tuser.send("Invalid command!\n")
        # if only one command was found, execute
        elif len(tcmd) == 1:
            tcmd[0].execute(tuser,cmds[1:])
        # or if multiple commands found, print them
        else:
            for c in tcmd:
                print c.cdict["name"]



