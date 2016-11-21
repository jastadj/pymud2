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
    cs.add("put", "Put something into something", doPutItem, True)
    cs.add("wield", "Wield a weapon", doWield, True)
    cs.add("unwield", "Unwield a weapon", doUnwield, True)
    cs.add("color", "Color on or off", doColor, True)
    cs.add("kill", "Kill target", doKill, True)
    
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
    
    tuser.send("Invalid command!\n")
    
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

    tuser.send("#C%dHelp Menu\n" % COLOR_MAGENTA )
    tuser.send("#c%d---------\n" % COLOR_MAGENTA )
    tuser.send("#c%d" %COLOR_GREEN )
    for i in range(0, tset.count() ) :
        tuser.send("%s - %s\n" %(tset.commands[i].cdict["name"], tset.commands[i].cdict["helpstring"]) )
    tuser.send("#cr")

def doColor(tuser, cdict, *argv):
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

    dolookin = False

    # remove the word "at"
    if "at" in args: args.remove("at")
            
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

    tobj = None

    # check mobs in room
    tmobs = findMobsInList(monoarg, troom.getMobs())
    if tmobs != None:
        tobj = tmobs[0]
    
    
    # items
    if tobj == None:
        titems = None
        
        # check items in room
        titems = findItemsInList(monoarg, troom.getItems())
        if titems != None:
            tobj = titems[0]

        # check items in inventory
        titems = findItemsInList(monoarg, tuser.char.getInventory())
        if titems != None:
            tobj = titems[0]
  
    if tobj != None:
        tuser.send("%s\n" %tobj.getDescription())
        
        # if container, show items it's holding
        if( issubclass( type(tobj), game.OBJECT_CLASSES["Item"]) ):
            if tobj.isContainer():
                
                # get item count of container
                icnt = len(tobj.getItems())
                
                # if container is empty
                if icnt == 0:
                    tuser.send("It is currently empty.\n")
                
                # else print its contents
                else:
                    tuser.send("It contains:\n")
                    for i in tobj.getItems():
                        tuser.send("    %s\n" %i.getExName() )
        
    else:
        tuser.send("You do not see that here.\n")


def doLookRoom(tuser, troom):
    if troom == None:
        tuser.send("Invalid room look - room is null!\n")
        return

    tuser.send("#C%d%s#cr\n" %(COLOR_CYAN,troom.getName()) )
    tuser.send("#C%d" %COLOR_BLACK)
    desclines = fitStringToWidth(troom.getDescription())
    for l in desclines:
        tuser.send("%s\n" %l)
    tuser.send("#cr")

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
        tuser.send("    %s\n" %i.getExName() )
        
    # list players and mobs here
    charlist = []
    charlist += troom.getMobs()
    for m in charlist:
        tuser.send("    %s is here.\n" %m.getExName())

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

def mobSay(tmob, saystr):
    
    troom = tmob.getCurrentRoom()
    
    if troom == None:
        print "Error in mobsay, mob has no current room!"
        return
        
    broadcastToRoom(troom, "%s says \"%s\"\n" %(tmob.getExName(),saystr) )
    
def doSay(tuser, cdict, *argv):
    args = []
    if argv[0] == None:
        args = None
    else:
        for a in argv[0]:
            args.append(a)

    if args:

        # get current room
        #troom = getCurrentRoom(tuser)

        # get all players in room
        #ulist = troom.getAllClientsInRoom(troom)

        # all arguments = say string
        troom = getCurrentRoom(tuser)
        saystr = " ".join(args)
        usaystr = "You say \"%s\"\n" %saystr
        saystr = "%s says \"%s\"\n" %(tuser.char.getExName(), saystr)
        
        broadcastToRoom(troom, saystr, tuser, usaystr )

    else:
        tuser.send("Say what?\n")

def getZoneFromRoom(troom):
    
    for z in game.zones:
        if z.hasRoom(troom):
            return game.zones.index(z)
    
    return None

def getAllClientsInRoom(troom):
    
    tzonenum = getZoneFromRoom(troom)
    
    clist = []
    
    if tzonenum == None:
        return None
    
    troomnum = game.zones[tzonenum].getRoomNum(troom)
    
    if troomnum == None:
        return None
    
    for u in game.clients:
        
        # make sure client has a character
        if u.char == None:
            continue
        
        if u.char.getCurrentRoom() == troomnum:
            if u.char.getCurrentZone() == tzonenum:
                clist.append(u)
    
    return clist
    

def broadcastToRoom(troom, tmsg, tuser = None, umsg = None):

    if troom == None:
        print "Error broadcasting to room, room is null!"
        return
   
    ulist = getAllClientsInRoom(troom)
    
    for u in ulist:
        if tuser != None:
            if tuser == u:
                if umsg != None:
                    tuser.send("%s" %  umsg)
                else:
                    tuser.send("%s" % tmsg )
                
        else: u.send("%s" %tmsg)

def getCurrentRoom(tuser):
    
    if issubclass(type(tuser), game.OBJECT_CLASSES["Mob"]):
        return tuser.getCurrentRoom()
    
    if issubclass(type(tuser), game.OBJECT_CLASSES["Client"]):
        
        crnum = tuser.char.getCurrentRoom()
        tz = getCurrentZone(tuser)
        tr = None

        try:
            tr = tz.rooms[crnum]
        except:
            print "Error getting current player room @ room #%d!!" %crnum
            return None

        return tr
    
    if issubclass(type(tuser), game.OBJECT_CLASSES["Character"]):
        return getCurrentRoom( tuser.getClient())

def getCurrentZone(tuser):

    tz = None
    pzi = tuser.char.getCurrentZone()

    try:
        tz = game.zones[pzi]
    except:
        print "Error getting current zone, index %d out of range!" %pzi
        return None

    return tz

def newItem(idesc):
    
    titem = findItemInList(idesc, game.items)
    
    if titem != None:
        return copy.deepcopy(titem)
    else:
        return None

def findItemInList(idesc, ilist = game.items):
    
    foundlist = []
    
    for i in ilist:
        if i.hasMatch(idesc):
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

def findItemsInList(idesc, ilist = game.items):
    
    foundlist = []
    
    for i in ilist:
        if i.hasMatch(idesc):
            foundlist.append(i)
    
    if len(foundlist) == 0:
        #print "Could not find item with \"%s\"" %idesc
        return None
    
    else:
        return foundlist

def findItemsInString(tstring):
    ilist = []
    
    words = tstring.split()
    
    wpos = 0
    
    for w in range(1, len(words) + 1 ):
        ifind = findItemsInList(" ".join(words[wpos:w]), game.items)
        
        if ifind != None:
            ilist.append(ifind[0])
            wpos = w
    
    return ilist
    

def doShowInventory(tuser, cdict):
    tuser.send("\n")
    
    # if wielding something
    if tuser.char.weaponSlots["right hand"] != None:
        tuser.send("You are wielding %s in your right hand.\n" %tuser.char.weaponSlots["right hand"].getExName() )
    if tuser.char.weaponSlots["left hand"] != None:
        tuser.send("You are wielding %s in your left hand.\n" %tuser.char.weaponSlots["left hand"].getExName() )        
        
    tuser.send("You are carring:\n")
    
    titems = tuser.char.getInventory()
    if len(titems) == 0:
        tuser.send("    Nothing!\n")
    else:
        for i in titems:
            tuser.send("    %s\n" %i.getExName() )

"""
def actorGet(tuser, tactor, istring):

    # current room
    troom = getCurrentRoom(tuser)
    if troom == None:
        print "ERROR do look, current room NULL!"
        return False

    ritems = troom.getItems()

    # look for item
    titems = findItemsInList(istring, ritems)
    
    # no items by that string were found in current room
    if titems == None:
        if tuser == tactor:
            tuser.send("You do not see that here.\n")
        
        return False
    # item found, get it and add to player inventory, remove from list
    # for now, just use the first item in list
    else:
        
        # remove item from room
        troom.removeItem(titems[0])
        
        # add item to target actor
        tactor.addItem(titems[0])
        
        ustr = "You take the %s.\n" %titems[0].getExName()
        tstr = "%s takes a %s.\n" %(tactor.getName(), titems[0].getExName())
        
        broadcastToRoomEx(tuser, tstr, tuser, ustr )
        
        return True
"""

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

    
    getfromcontainer = False
    
    # check if getting an item from something
    if "from" in args:
        args.remove("from")
        getfromcontainer = True
    

    # get a string from args
    monoarg = " ".join(args)
    
    # multiple items in arguments
    multitems = None
    
    multitems = findItemsInString(monoarg)
    if len(multitems) == 2:
        getfromcontainer = True
        

    # current room
    troom = getCurrentRoom(tuser)
    if troom == None:
        print "ERROR do look, current room NULL!"
        return

    ritems = troom.getItems()

    # if getting item from container
    if getfromcontainer:
        
        if len(multitems) != 2:
            tuser.send("Get what from what?\n")
            return
        
        # get user inventory
        invitems = tuser.char.getInventory()
        
        # get item names
        citemname = multitems[1].getExName()
        tgtitemname = multitems[0].getExName()
        
        # check that container is in inventory
        citem = findItemsInList(citemname, invitems)
        if citem == None:
            tuser.send("You do not have that!\n")
            return
        else:
            citem = citem[0]
        
        # check that target item is in container
        citemlist = citem.getItems()
        
        tgtitem = findItemsInList(tgtitemname, citemlist)
        if tgtitem == None:
            tuser.send("You do not see that!\n")
            return
        else:
            tgtitem = tgtitem[0]
        
        #remove target item from container
        citem.removeItem(tgtitem)
        
        # add target item to user inventory
        tuser.char.addItem(tgtitem)
        
        # give feedback
        tuser.send("You take %s from %s.\n" %(tgtitem.getExName(), citem.getExName()) )
        return


    # look for item
    titems = findItemsInList(monoarg, ritems)
    
    if titems == None:
        tuser.send("You do not see that here.\n")
    # item found, get it and add to player inventory, remove from list
    else:
        troom.removeItem(titems[0])
        tuser.char.addItem(titems[0])
        
        ustr = "You take the %s.\n" %titems[0].getExName()
        tstr = "%s takes a %s.\n" %(tuser.char.getName(), titems[0].getExName())
        
        broadcastToRoom(troom, tstr, tuser, ustr )
        
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
        ustr = "You drop the %s.\n" %titems[0].getName()
        tstr = "%s drops %s.\n" %(tuser.char.getName(), titems[0].getExName())

        broadcastToRoom(troom, tstr, tuser, ustr )
        
        return True

def doPutItem(tuser, cdict, *argv):
    args = []
    # no arguments, do a room look
    if argv[0] == None:
        tuser.send("Put what?\n")
        return False
    # arguments
    else:
        for a in argv[0]:
            args.append(a)

    # remove into or in words
    if "in" in args:
        args.remove("in")
    if "into" in args:
        args.remove("into")

    # get a string from args
    monoarg = " ".join(args)
    
    
    fitems = findItemsInString(monoarg)
        
    if len(fitems) != 2:
        tuser.send("Put what into what?\n")
        return
    
    tgtitemname = fitems[0].getExName()
    tgtitem = None
    conitemname = fitems[1].getExName()
    conitem = None
    
    # get room and inventory item lists
    troom = getCurrentRoom(tuser)
    invlist = tuser.char.getInventory()
    rlist = troom.getItems()
    
    
    # check if target item is in inventory
    tgtitem = findItemsInList(tgtitemname, invlist)
    if tgtitem == None:
        tuser.send("You do not have that!\n")
        return
    else:
        tgtitem = tgtitem[0]
    
    # check if container is in inventory or room
    conitem = findItemsInList(conitemname, invlist)
    if conitem == None:
        
        conitem = findItemsInList(conitemname, rlist)
        
        if conitem == None:
            tuser.send("You do no have that!\n")
            return
    
    conitem = conitem[0]
    
    # check that second item is a container
    if not conitem.isContainer():
        tuser.send("That is not a container!\n")
        return
    
    
    # remove target item from player inventory
    tuser.char.removeItem(tgtitem)
    
    # put target item into container
    conitem.addItem(tgtitem)
        
    tuser.send("You put %s into %s.\n" %(tgtitem.getExName(), conitem.getExName()) )
            

def doWield(tuser, cdict, *argv):
    args = []
    # no arguments, do a room look
    if argv[0] == None:
        tuser.send("Wield what?\n")
        return False
    # arguments
    else:
        for a in argv[0]:
            args.append(a)
    
    monoarg = " ".join(args)
    pitems = tuser.char.getInventory()
    tweapon = findItemsInList(monoarg, pitems)
    
    # couldn't find target weapon
    if tweapon == None:
        tuser.send("You do not have that!\n")
        return False
    
    tweapon = tweapon[0]
    
    result = tuser.char.wield(tweapon)
    
    # if wield returns with a string, wield didn't
    # happen, string is feedback
    if type(result) == str:
        tuser.send("%s\n" %result)
        return False
    # if bool is returned true, wield was successful
    elif type(result) == bool:
        if result != True:
            print "Error, returning a False bool on wield unexpected!"
            return
        # wielded successfuly, give feedback on which hands were used
        if tweapon.getHands() == 2:
            tuser.send("Wielded %s in both hands.\n" %tweapon.getExName())
        else:
            for s in tuser.char.weaponSlots.keys():
                if tuser.char.weaponSlots[s] == tweapon:
                    tuser.send("You wield %s in your %s.\n" %(tweapon.getExName(), s) )
                    return True
            
            # weapon was not found in weapon slot??
            print "Error, could not find wielded weapon in any weapon slot!"
            return False
    else:
        print "Unexpected return type on actor wield = %s" %type(result)
        return False
            

def doUnwield(tuser, cdict, *argv):
    args = []
    # no arguments, do a room look
    if argv[0] == None:
        tuser.send("Wield what?\n")
        return False
    # arguments
    else:
        for a in argv[0]:
            args.append(a)
    
    monoarg = " ".join(args)
    pitems = tuser.char.getWielded()
    tweapon = findItemsInList(monoarg, pitems)
    
    # couldn't find target weapon
    if tweapon == None:
        tuser.send("You are not wielding that!\n")
        return False
    
    tweapon = tweapon[0]
    
    # unwield weapon
    tuser.char.addItem( tweapon)
    tuser.char.weaponSlots["right hand"] = None
    if tuser.char.weaponSlots["left hand"] == tweapon:
        tuser.char.weaponSlots["left hand"] = None
    tuser.send("You unwield the %s.\n" %tweapon.getName())
    
def newMob(mdesc):
    
    tmob = findMobInList(mdesc, game.mobs)
    
    if tmob != None:
        return copy.copy(tmob)
    else:
        return None

def findMobsInList(mdesc, mlist = game.mobs):
    
    foundlist = []
    
    for m in mlist:
        if m.hasMatch(mdesc):
            foundlist.append(m)
    
    if len(foundlist) == 0:
        #print "Could not find mob with \"%s\"" %mdesc
        return None
    
    else:
        return foundlist

def findMobInList(mdesc, mlist = game.mobs):
    
    foundlist = []
    
    for m in mlist:
        if m.hasMatch(mdesc):
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

def doKill(tuser, cdict, *argv):
    args = []
    # no arguments, do a room look
    if argv[0] == None:
        tuser.send("Attack who?\n")
        return
    # arguments
    else:
        for a in argv[0]:
            args.append(a)

    monoarg = " ".join(args)
    
    # get current room of user
    troom = getCurrentRoom(tuser)
    
    # get list of mobs in current room
    mlist = troom.getMobs()
    
    tmob = findMobsInList(monoarg, mlist)
    
    if tmob == None:
        tuser.send("You do not see that here!\n")
        return
    
    else:
        tmob = tmob[0]
        
        tuser.send("You start attacking %s!\n" %tmob.getExName())
        tuser.char.setCombatTarget(tmob)
        tmob.setCombatTarget(tuser.char)

def doAttack(tactor):
    
    if not tactor.inCombat():
        print "Error doAttack, tactor not in combat!"
        return
    
    opponent = tactor.getCombatTarget()
    troom = getCurrentRoom(tactor)
    
    # check that target is in room
    if troom != getCurrentRoom(opponent):
        
        #is target dead?
        if not opponent.isAlive():
            opponent.setCombatTarget(None)
            tactor.setCombatTarget(None)
        
        return
    
    dodmg = getAttackRoll(tactor)
    
    tmsg = "%s attacks %s for %d damage.\n" %(tactor.getExName(), opponent.getExName(), dodmg)
    umsg = ""
    
    # if attacker is player
    if tactor.isPlayer():
        umsg = "You attack %s for %d damage.\n" %(opponent.getExName(), dodmg)
        broadcastToRoom(troom, tmsg, tactor.getClient(), umsg)
    
    # if opponent is player
    elif opponent.isPlayer():
        umsg = "%s hits you for %d damage.\n" %(tactor.getExName(), dodmg)
        broadcastToRoom(troom, tmsg, opponent.getClient(), umsg)
    
    # else player is witnessing
    else:
        broadcastToRoom(troom, tmsg)
    
    # apply damage
    addHealth(opponent, -dodmg)
    

def getAttackRoll(tactor):
    
    weps = tactor.getWielded()
    
    if len(weps) == 0:
        return 1
    
    dmgtot = 0
    
    for w in weps:
        dmgtot += w.getDamage()
    
    return dmgtot

def addHealth(tactor, amount):
    
    currenthp = tactor.getAttribute("current hp")
    
    tactor.setAttribute("current hp", currenthp + amount)
    

#####################################################################
if __name__ == "__main__":
    import gameinit
    gameinit.gameInitTest()
    
    teststring = "long sword cloth bag"
    
    
    titems = findItemsInString(teststring)
    
    print "Finding items in string:%s" %teststring
    
    for i in titems:
        print i.getExName()


