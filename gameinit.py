import defs
import credential
import testclient
import game
import worldobject
import item
import room
import zone
import command
import character
import weapon
import armor
import mob

from tools import *


def addObjectClass(tobj):
    game.OBJECT_CLASSES.update( {tobj().__class__.__name__:tobj} )

def gameInit():
    
    # game callbacks
    addObjectClass(item.Item)
    addObjectClass(weapon.Weapon)
    addObjectClass(armor.Armor)
    addObjectClass(character.Character)
    addObjectClass(mob.Mob)
    #addObjectClass(room.Room)

    game.ZONE = zone.Zone

    game.COMMAND = command.Command
    game.COMMAND_SET = command.CommandSet


    #zero lists
    game.items = []
    game.mobs = []
    game.zones = []
    
    # load credentials
    credential.loadCredentials()
    
    # load commands
    game.cmds_main = command.initMainCommands()
    game.cmds_main.setInvalidFunction( command.mainGameInvalid )
    
    
    # load items
    loadItems()

    # load mobs
    #mob.loadMobs()
    
    # load zones
    #zone.loadZones()
    
    # feedback
    print "%d accounts loaded." %len(game.credentials)
    print "%d commands loaded." %len(game.cmds_main.commands)    
    print "%d items loaded." %len(game.items)
    print "%d mobs loaded." %len(game.mobs)
    print "%d zones loaded." %len(game.zones)
    


def gameInitTest():
    # load test configuration
    defs.TEST_MODE = True
    defs.configTestMode()
    
    gameInit()
    
    # create test user
    tuser = testclient.TestClient()
    tuser.setMode("login0")
    game.clients = []
    game.clients.append(tuser)
    print "TestUser created..."

#################################
#
#   COMMON ITEMS SAVE/LOAD

def saveItems():
    
    fp = defs.ITEMS_FILE
    
    createNewFile(fp)
    
    f = open(fp, "w")
    
    for i in game.items_common:
        ilines = i.saveToStrings()
        
        for line in ilines:
            f.write("%s\n" %line)
        
        f.write("\n")
    
    f.close()

def loadItems():
    
    fp = defs.ITEMS_FILE
    
    game.items_common = []
    
    otypes = game.OBJECT_CLASSES
       
    # if items file exists
    if createNewFile(fp) == None:
        
        with open(fp, "r") as f:
            for line in f:
                
                # trim newline
                line = line[:-1]
                
                # if line is blank
                if line == "": continue
                
                ifind = line.find(':')
                key = line[:ifind]
                val = line[ifind+1:]
                
                
                # if item entry found, create item type
                if key == "item":
                    
                    game.items_common.append( otypes[val]() )
                
                # else, process each line as a load string
                if len(game.items_common) != 0:
                    game.items_common[-1].loadFromStrings( [line] )
        
        f.close()
        
    # items file does not exist
    else:
        pass
    
    # transfer loaded common items to main game items
    game.items += game.items_common


#################################
#
#   COMMON MOBS SAVE/LOAD

def saveMobs():
    
    fp = defs.MOBS_FILE
    
    createNewFile(fp)
    
    f = open(fp, "w")
    
    #write each mob's savestrings to file
    for m in game.mobs_common:
        
        mlines = saveToStrings(m)
        
        for line in mlines:
            f.write("%s\n" %line)
        
        f.write("\n")
    
    f.close()
        
def loadMobs():
    
    fp = defs.MOBS_FILE
    
    game.mobs_common = []
    
    otypes = game.OBJECT_CLASSES    
    
    # if file already exists
    if createNewFile(fp) == None:
        
        mlines = []
        
        # open file for reading
        with open(fp, "r") as f:
            
            # check each line in file
            for line in f:
                
                # trim new line
                line = line[:-1]
                
                # ignore blank lines
                if line == "": continue

                delim = line.find(':')
                key = line[:delim]
                val = line[delim+1:]

                # if actor entry found, create actor type
                if key == "actor":
                    
                    game.mobs_common.append( otypes[val]() )
                
                # else, process each line as a load string
                if len(game.mobs_common) != 0:
                    game.mobs_common[-1].loadFromStrings( [line] )

                        
        # done
        f.close()
    
        # append common mobs to main mobs list
        game.mobs += game.mobs_common
    
    # else file doesnt exist
    else:
        pass

#################################
#
#   ZONES SAVE/LOAD

def saveZones():
    
    zones = game.zones
    
    # if necessary, create new zone index file
    createNewFile(defs.ZONES_INDEX_FILE)
    
    # save each zone
    for z in zones:
        z.save()
        
    # write zone index file
    f = open(defs.ZONES_INDEX_FILE, "w")
    
    for z in zones:
        f.write(z.zonefile + "\n")
    f.close()
    
def loadZones():
     
    zf = defs.ZONES_INDEX_FILE
    
    #debug
    #print "loading zone index file : %s" %zf
    
    game.zones = []
    
    zonefiles = []
 
     # if file exists
    if createNewFile(zf) == None:
        
        
        #read in index files
        with open(zf, "r") as f:
            
            for line in f:
                
                # trim new line
                if line[-1] == '\n':
                    line = line[:-1]
                
                # if line isn't blank, add it to zonefile list
                if line != "":
                    #print line
                    zonefiles.append(line)
            
        f.close()
                
        # load in each zone from file
        for zt in zonefiles:
            newzone = Zone()
            newzone.load(zt)
            game.zones.append(newzone)
    
    # else file is new, create defaults
    else:
        
        print "No zones present.  Creating default zone..."
        # create default zone and room
        newzone = Zone()
        newzone.addRoom( room.Room())
        newzone.zonefile = "default.zn"
        newzone.save()
        # add this zone to zonelist
        game.zones.append(newzone)
        
        # save zonelist
        saveZones()
    

        


if __name__ == "__main__":
    gameInitTest()
