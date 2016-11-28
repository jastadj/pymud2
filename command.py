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

        # if string was a directional (n,e,s,w,etc..)
        if cstr in ["n", "s", "e", "w"]:
            return None

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
    cd.add("put", "Put an item into something", doputitem, True)
    cd.add("wield", "Wield a weapon", dowield, True)
    cd.add("unwield", "Unwield a weapon", dounwield, True)
    cd.add("score", "Show player info", doscore, False)
    cd.add("kill", "Kill target", dokill, True)
    cd.add("eat", "Eat something", doeat, True)
    cd.add("drink", "Drink something", dodrink, True)
    
    cd.add("debug", "Do a debug #", dodebug, True)
    cd.add("showuid", "Show object of uid#", dodebugshowuid, True)
    cd.add("showiid", "Show object instance of iid#", dodebugshowiid, True)
    #cd.add("showroom", "Show current room info", dodebugshowcurrentroom, False)
    
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
            tuser.send("%d : %s (%s)\n" %(o, hub.worldobjects_instance[o].getnameex(), hub.worldobjects_instance[o].gettype() ) )
        
        try:
            tempval = hub.worldobjects_instance.keys()[0]
            iidcounter = hub.worldobjects_instance[tempval].iidcount
            tuser.send("iidcounter = %d\n" %iidcounter)
        except:
            pass
        
        tuser.send("%d world instance objects.\n" %len(hub.worldobjects_instance.keys() ) )            
    
    if debugmode == 2:
        hub.showworldobjects("room")

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

def gettargetobjfromargs(tuser, tlist, args):
    
    # target item number ( for multiples)
    itemnum = 0
    
    # if item number supplied in args
    try:
        itemnum = int(args[-1]) - 1
        args = args[:-1]
        if itemnum < 0: itemnum = 0
    except:
        itemnum = 0
    
    # get string from supplied arguments
    monoarg = " ".join(args)
    
    # look for target item in list
    foundcount = 0
    for i in tlist:
        if i.getref().hasmatch(monoarg):
            
            # skip item
            if foundcount != itemnum:
                foundcount += 1
                continue
            
            # return found item
            return i
    
    
    return None

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
##      COMBAT

def docombat(tactor):
    
    tactor.combatticks -= 1
    
    # if actor ready to attack
    if tactor.combatticks <= 0:
        
        troom = tactor.getroom()
        
        tactor.combatticks = tactor.getcombatspeed()
        
        tdmg = tactor.getattackroll()
        
        ctarget = tactor.combattarget
        
        
        cmsg = "%s hits %s for %d damage.\n" %(tactor.getnameex(), ctarget.getnameex(), tdmg)
        aggmsg = "You hit %s for %d damage.\n" %(ctarget.getnameex(), tdmg)
        defmsg = "%s hits you for %d damage.\n" %(tactor.getnameex(), tdmg)
        
        
        ctarget.takehit(tdmg)
        
        for c in getallclientsinroom(troom):
            if c.char == tactor:
                c.send(aggmsg)
            elif c.char == ctarget:
                c.send(defmsg)
            else:
                c.send(cmsg)
       

def dokill(tuser, cdict, *argv):
    args = []
    # no arguments, do a room look
    if argv[0] == None:
        pass
    # arguments
    else:
        for a in argv[0]:
            args.append(a)
    
    if len(args) == 0:
        tuser.send("Kill what?\n")
        return
    
    monoarg = " ".join(args)
    
    troom = getcurrentroom(tuser)
    tmob = None
    
    # check that target mob is in the room
    for m in troom.getmobs():
        if m.getref().hasmatch(monoarg):
            tmob = m
            break
    
    # mob found, attack mob
    if tmob != None:
        
        tmob.setcombattarget(tuser.char)
        tuser.char.setcombattarget(tmob)
        
        tmsg = "%s starts fighting %s!\n" %(tuser.char.getnameex(), tmob.getref().getnameex())
        umsg = "You start fighting %s\n" %(tmob.getref().getnameex())
        doroombroadcast(troom, tmsg, tuser, umsg)

        
        """
        # get attack damage
        attackval = tuser.char.getattackroll()
        
        # apply attack damage to target mob
        tmob.takehit(attackval)
        
        tmsg = "%s hits %s for %d\n" %(tuser.char.getnameex(), tmob.getref().getnameex(), attackval)
        umsg = "You hit %s for %d\n" %(tmob.getref().getnameex(), attackval)
        doroombroadcast(troom, tmsg, tuser, umsg)
        """
    
    else:
        tuser.send("You do not see that here!\n")
        return False


###########################################
##      CHARACTER

def doscore(tuser, cdict):
    
    tstrings = ""
    
    tstrings += "Name : %s\n" %tuser.char.getnameex()
    
    tstrings += "HP : %d/%d\n" %(tuser.char.getattribute("hp"), tuser.char.getattribute("maxhp"))
    
    tuser.send(tstrings)

def doinventory(tuser, cdict):
    
    tstrings = []
    
    tinv = tuser.char.getinventory()
    
    twielded = tuser.char.getwielding()
    
    tstrings += "You are wielding "
    if tuser.char.getwielding() == None:
        tstrings += "nothing.\n"
    else:
        tstrings += tuser.char.getwielding().getref().getnameex() + ".\n"
    
    
    tstrings += "You are carring:\n"
    
    if len(tinv) == 0:
        tstrings += "  Nothing!\n"
    else:
        for i in tinv:
            if twielded == i:
                pass
            else:
                tstrings += "  %s\n" %i.getnameex()

    
    tuser.send(tstrings)

def dowield(tuser, cdict, *argv):
    args = []
    # no arguments, do a room look
    if argv[0] == None:
        pass
    # arguments
    else:
        for a in argv[0]:
            args.append(a)
    
    if len(args) == 0:
        tuser.send("Wield what?\n")
        return False
        
    titem = gettargetobjfromargs(tuser, tuser.char.getinventory(), args)
    troom = getcurrentroom(tuser)
    
    if titem != None:

        # check if item is a weapon
        if not titem.getref().isweapon():
            tuser.send("That is not a weapon!\n")
            return False
        
        # check is wielding something
        if tuser.char.getwielding() != None:
            tuser.send("You are already wielding a weapon!\n")
            return False
        
        # wield weapon
        tuser.char.wield(titem)
        
        tmsg = "%s wields %s.\n" %(tuser.char.getnameex(), titem.getref().getnameex())
        umsg = "You wield %s.\n" %titem.getref().getnameex()
        doroombroadcast(troom, tmsg, tuser, umsg)
        
        return True

    tuser.send("You do not have that!\n")
    return False

def dounwield(tuser, cdict, *argv):
    args = []
    # no arguments, do a room look
    if argv[0] == None:
        pass
    # arguments
    else:
        for a in argv[0]:
            args.append(a)
    
    if len(args) == 0:
        tuser.send("Unwield what?\n")
        return False
        
    titem = gettargetobjfromargs(tuser, tuser.char.getequipped(), args)
    troom = getcurrentroom(tuser)
    
    if titem != None:

        # check that item is wielded
        if titem != tuser.char.getwielding():
            tuser.send("You are not wielding that!\n")
            return False
        
        # wield weapon
        tuser.char.unwield(titem)
        
        tmsg = "%s unwields %s.\n" %(tuser.char.getnameex(), titem.getref().getnameex())
        umsg = "You unwield %s.\n" %titem.getref().getnameex()
        doroombroadcast(troom, tmsg, tuser, umsg)
        
        return True

    tuser.send("You do not have that!\n")
    return False


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
    
    while True:
        # check if item in inventory
        tobj = gettargetobjfromargs(tuser, tuser.char.getinventory(), args)
        if tobj != None:
            break

        tobj = gettargetobjfromargs(tuser, tuser.char.getinventoryandequipment(), args)
        if tobj != None:
            break

        tobj = gettargetobjfromargs(tuser, troom.getitems(), args)
        if tobj != None:
            break
        
        tobj = gettargetobjfromargs(tuser, troom.getmobs(), args)
        if tobj != None:
            break
        
        # check room descriptors
        if monoarg in troom.getdescriptors():
            descstr = troom.getdescriptors()[monoarg]
            tuser.send("%s\n" %descstr)
            return
        
        break
        
    if tobj != None:
        descstr = tobj.getlookstr()
        tuser.send("%s" %descstr)
        return
    else:
        tuser.send("You do not see that here!\n")

        
    

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
        
    troom = getcurrentroom(tuser)
    titem = gettargetobjfromargs(tuser,troom.getitems(), args)
    
    # if object was found
    if titem != None:

        # remove item from room
        troom.removeitem(titem)
        
        # add item to player
        tuser.char.additem(titem)
        
        tmsg = "%s picks up %s.\n" %(tuser.char.getnameex(), titem.getref().getnameex() )
        umsg = "You pick up %s.\n" %titem.getref().getnameex()
        
        doroombroadcast(troom, tmsg, tuser, umsg)
        
        return True
    # else if object wasn't found, try to see if object was "get" from container
    else:
        
        while True:
            # remove just words
            if "from" in args:
                args.remove("from")
                
            item1 = None
            item2 = None
            
            # get item 2
            spos = 1
            for a in reversed(range(1, len(args)+1)):
                
                # first try searching inventory
                titem = gettargetobjfromargs(tuser, tuser.char.getinventory(), args[a:])
                
                # try searching room items
                if titem == None:
                    titem = gettargetobjfromargs(tuser, troom.getitems(), args[a:])
                
                # if item was found
                if titem != None:
                    item2 = titem
                    spos = a
                    break
            
            # no item found
            if item2 == None:
                break
            
            # first object string = arguments - second object string
            args2 = args[:spos]
            
            # get item 1 from item 2
            item1 = gettargetobjfromargs(tuser, item2.container.getitems(), args2)
            if item1 != None:
                
                #remove item1 from item 2
                item2.container.removeitem(item1)
                
                # add item1 to player inventory
                tuser.char.additem(item1)
                
                # feeback
                tmsg = "%s gets %s from %s.\n" %(tuser.char.getnameex(), item1.getnameex(), item2.getnameex())
                umsg = "You take %s from %s.\n" %(item1.getnameex(), item2.getnameex())
                doroombroadcast(troom, tmsg, tuser, umsg)
                
                return True
            else:
                tuser.send("You do not see that there.\n")
                return False
            break

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
    
    if len(args) == 1:
        if args[0] == "all":
            for i in tuser.char.getinventory():
                dodropitem(tuser, cdict, i.getnameex().split())
            return True
    
    titem = gettargetobjfromargs(tuser, tuser.char.getinventory(), args)
    troom = getcurrentroom(tuser)
    
    if titem != None:

        # remove item from player inventory
        tuser.char.removeitem(titem)
        
        # add item to room
        troom.additem(titem)
        
        tmsg = "%s drops %s.\n" %(tuser.char.getnameex(), titem.getref().getnameex())
        umsg = "You drop %s.\n" %titem.getref().getnameex()
        doroombroadcast(troom, tmsg, tuser, umsg)
        
        return True

    tuser.send("You do not have that!\n")
    return False    

def doputitem(tuser, cdict, *argv):
    args = []
    # no arguments, do a room look
    if argv[0] == None:
        pass
    # arguments
    else:
        for a in argv[0]:
            args.append(a)
    
    if len(args) == 0:
        tuser.send("Put what into what?\n")
        return False
        
    # remove junk words
    if "in" in args:
        args.remove("in")
    elif "into" in args:
        args.remove("into")
    
    item1 = None
    item2 = None
    
    # get item 1
    spos = 1
    for a in range(1, len(args)+1):
        titem = gettargetobjfromargs(tuser, tuser.char.getinventory(), args[:a])
        if titem != None:
            item1 = titem
            spos = a
            break
    
    args2 = args[spos:]
    
    # get item 2
    item2 = gettargetobjfromargs(tuser, tuser.char.getinventory(), args2)
    
    if item1 != None and item2 != None:
        if item2.getref().iscontainer():
            
            # remove item 1 from inventory
            tuser.char.removeitem(item1)
            
            # add item 1 to container 2
            item2.container.additem(item1)
            
            return True
    
    tuser.send("Put what into what?\n")
    return False

def doeat(tuser, cdict, *argv):
    args = []
    # no arguments, do a room look
    if argv[0] == None:
        pass
    # arguments
    else:
        for a in argv[0]:
            args.append(a)
    
    if len(args) == 0:
        tuser.send("Eat what?\n")
        return False    
        
    troom = getcurrentroom(tuser)
    
    # look for item in inventory first
    titem = gettargetobjfromargs(tuser, tuser.char.getinventory(), args)
    if titem != None:
        
        # remove item from inventory
        tuser.char.removeitem(titem)
    
    # else look for item in room
    else:
        titem = gettargetobjfromargs(tuser, troom.getitems(), args)
        
        if titem != None:
            
            # remove item from room
            troom.removeitem(titem)
    
    if titem == None:
        tuser.send("You do not see that!\n")
        return False
    
    # make sure item is edible
    if not titem.getref().isfood():
        tuser.send("That is not edible!\n")
        return False
    
    # eat item
    # ...
    
    # broadcast message
    tmsg = "%s eats %s.\n" %(tuser.char.getnameex(), titem.getnameex())
    umsg = "You eat %s.\n" %(titem.getnameex())
    doroombroadcast(troom, tmsg, tuser, umsg)

def dodrink(tuser, cdict, *argv):
    args = []
    # no arguments, do a room look
    if argv[0] == None:
        pass
    # arguments
    else:
        for a in argv[0]:
            args.append(a)
    
    if len(args) == 0:
        tuser.send("Drink what?\n")
        return False    
        
    troom = getcurrentroom(tuser)
    
    # look for item in inventory first
    titem = gettargetobjfromargs(tuser, tuser.char.getinventory(), args)
    if titem != None:
        
        # remove item from inventory
        tuser.char.removeitem(titem)
    
    # else look for item in room
    else:
        titem = gettargetobjfromargs(tuser, troom.getitems(), args)
        
        if titem != None:
            
            # remove item from room
            troom.removeitem(titem)
    
    if titem == None:
        tuser.send("You do not see that!\n")
        return False
    
    # make sure item is edible
    if not titem.getref().isdrink():
        tuser.send("That is not drinkable!\n")
        return False
    
    # drink item
    # ...
    
    # broadcast message
    tmsg = "%s drinks %s.\n" %(tuser.char.getnameex(), titem.getnameex())
    umsg = "You drink %s.\n" %(titem.getnameex())
    doroombroadcast(troom, tmsg, tuser, umsg)

###########################################
##      ROOM

def getcurrentroom(tuser):
    tzone = tuser.char.getcurrentzoneid()
    
    troom = hub.zones[tzone].getroom(tuser.char.getcurrentroomid())
    
    return troom    

def getallclientsinroom(troom):
    
    clist = []
    
    for c in hub.clients:
        if c.char.getroom() == troom:
            clist.append(c)
    
    return clist

def doroomlook(tuser, troom):

    tstrings = ""
        
    # print room name and desc
    tstrings += "#C6%s#cr\n" %troom.getname()
    tstrings += "#C0%s#cr\n" %troom.getdescription()
    
    # print exits
    if len(troom.getexits().keys()) == 0:
        tstrings += "There are no obvious exits.\n"
    else:
        tstrings += "Exits: "
        
        for e in troom.getexits().keys():
            tstrings += "%s " %e
        tstrings += "\n"
    
    for m in troom.getmobs():
        if m.incombat():
            tstrings += "    %s (in combat)\n" %m.getnameex()
        else:
            tstrings += "    %s\n" %m.getnameex()
    
    for i in troom.getitems():
        tstrings += "    %s\n" %i.getnameex()
        
    tuser.send(tstrings)
        
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



