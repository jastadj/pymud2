import defs

# class refs
COMMAND = None
COMMAND_SET = None
ITEM = None

# objects
server = None
timer = None
accounts = None
cmds_main = None

# lists
clients = []
commonitems = [] #this is used for saving/loading common items only
commonmobs = [] # this is used for saving/loading common mobs only

# dicts, stores all items by uid, and all item instances by iid
worldobjects = {}
worldobjects_specific = {}
worldobjects_instance = {}

zones = {}


def addworldobject(tobj):
    
    # get dict entry of world object
    tdict = {tobj.getuid():tobj}
    
    objtype = tobj.gettype()
    
    # update master world objects list
    worldobjects.update( tdict )
    
    # update specific object list
    if not objtype in worldobjects_specific.keys():
        worldobjects_specific.update( {objtype:{}} )
    worldobjects_specific[objtype].update(tdict)
        
def addworldinstanceobject(tiobj):
    # get dict entry of world object
    tdict = {tiobj.getiid():tiobj}
    
    
    # update master world objects list
    worldobjects_instance.update( tdict )

def finduidbyname(tdesc):
    for o in worldobjects.keys():
        if worldobjects[o].hasmatch(tdesc):
            return o
    return None

def findworldobjectbyname(tdesc):
    tobj = finduidbyname(tdesc)
    
    if tobj != None:
        return worldobjects[tobj]
    
    return None
        
def showworldobjects(specific = None):
    
    if specific == None:
        print "World Objects:"
        print "--------------"
        for o in worldobjects.keys():
            print "  %d:%s (%s)" %( o, worldobjects[o].getname(), worldobjects[o].gettype())
    else:
        
        if not specific in worldobjects_specific:
            print "World Objects Specific does not contain %s type!" %specific
            return
        
        print "World Objects of Type:%s" %specific
        print "----------------------" + "-"*len(specific)
        for o in worldobjects_specific[specific].keys():
            print "  %d:%s" %(o, worldobjects_specific[specific][o].getname() )

def createobject(uid):
    
    objref = None
    tobj = None
    try:
        objref = worldobjects[uid]
        tobj = objref.create()
    except:
        return None
        
    return tobj

def lobby(tuser):
    
    do_passes = 0
    
    while do_passes >= 0:
        
        if tuser.mode == "lobby":
            
            
            cmds = tuser.getlastinput().split()
            
            if len(cmds) > 0:
                pass
            
            tuser.send("echo:%s\n" %tuser.getlastinput())
            tuser.send(">")
        
        do_passes -= 1 

# main
def maingame(tuser):
    
    do_passes = 0
    
    while do_passes >= 0:
        
        if tuser.mode == "maingame":
            
            cmds = tuser.getlastinput().split()
            
            if len(cmds) > 0:
                
                # process main game command
                tcmd = cmds_main.getcommand(cmds[0])
                
                # no valid command found
                if tcmd == None:
					cmds_main.getinvalidfunction()(tuser)
                # exactly one command found, execute
                elif len(tcmd) == 1:
                    tcmd[0].execute(tuser, cmds[1:])
                # multiple commands found, print them
                else:
                    for c in tcmd:
                        tuser.send("%s\n" %c)
            
            tuser.send(">")
            
            
        # if entering the game after login
        elif tuser.mode == "maingamestart":
            cmds_main.getandexecute(tuser, "look")
            tuser.mode = "maingame"
            do_passes = 1
        
        do_passes -= 1

  
    
