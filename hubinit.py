import json
import defs
import timer
from tools import *
import account
import client
import testclient
import hub
import command
import worldobject
import item

import zone

from tools import *

def hubinit():

    # clear lists
    hub.clients = []
    
    # load persistent data file
    loadpersistentdata()
    
    # load accounts
    hub.accounts = account.accountmanager()
    
    # load commands
    hub.cmds_main = command.initmaincommands()
    hub.cmds_main.setinvalidfunction( command.maingameinvalid )
        
    # timer
    hub.timer = timer.timer()
    print "Timer start:%f" %hub.timer.getstarttime()
    
    # load items
    #hub.ITEM = item.item
    #loaditems()
    
    # load zones
    loadzones()


    # init summary
    print "Loaded %d accounts." %hub.accounts.count()
    print "Loaded %d zones." %len(hub.zones.keys())
    #print "Loaded %d items." %len(hub.commonitems)

def hubinittest():
    # load test configuration
    defs.TEST_MODE = True
    defs.configtestmode()
    
    hubinit()
    
    # create test user
    tuser = testclient.testclient()
    tuser.setmode("login0")
    hub.clients = []
    hub.clients.append(tuser)
    print "TestUser created..."


def save():
    
    #print "Saving items..."
    #saveitems()
    print "Saving accounts..."
    hub.accounts.save()
    print "Saving zones..."
    savezones()
    print "Saving persistent data..."
    savepersistentdata()

def savepersistentdata():
    
    fp = defs.PERS_DATA_FILE
    
    createNewFile(fp)
    
    pdata = {}
    pdata.update( {"uidcount":worldobject.worldobject.uidcount} )
    pdata.update( {"iidcount":item.item.iidcount} )
    
    f = open(fp, "w")
    f.write( json.dumps(pdata) + "\n")
    f.close()
    

def loadpersistentdata():
    
    fp = defs.PERS_DATA_FILE
    
    createNewFile(fp)
    
    with open(fp,"r") as f:
        for line in f:
            line = line[:-1]
            
            if line == "": continue
            
            jobj = json.loads(line)
            
            if "uidcount" in jobj.keys():
                worldobject.worldobject.uidcount = jobj["uidcount"]
            
            if "iidcount" in jobj.keys():
                item.item.iidcount = jobj["iidcount"]
                
    f.close()
    

#############################################
##      ITEMS

def saveitems():
    
    fp = defs.ITEMS_COMMON
    
    createNewFile(fp)
    
    f = open(fp, "w")
    
    for i in hub.commonitems:
        f.write( i.toJSON() + "\n")
    
    f.close()
        
def loaditems():
    
    fp = defs.ITEMS_COMMON
    
    createNewFile(fp)
    
    with open(fp, "r") as f:
        
        for line in f:
            
            line = line[:-1]
            
            if line == "": continue
            
            newitem = item.itemmaster("unnamed", True, line)
    
    f.close()


#############################################
##      ZONES

def savezones():
    
    fp = defs.ZONES_INDEX_FILE
    
    createNewFile(fp)
    
    f = open(fp, "w")
    
    for z in hub.zones.keys():
        
        # save zone index and filename to zone index file
        f.write("%d:%s\n" %(z, hub.zones[z].getfilename() ) )
        
        # save zone file
        hub.zones[z].save()
        
    f.close()

def loadzones():
    
    fp = defs.ZONES_INDEX_FILE
    
    # if file exists
    if createNewFile(fp) == None:
        with open(fp, "r") as f:
            for line in f:
                
                line = line[:-1]
                
                if line == "": continue
                
                delim = line.find(':')
                zid = int(line[:delim])
                filename = line[delim+1:]
                
                # check to make sure zone id doesn't already exist
                if zid in hub.zones.keys():
                    print "Zone ID %d already exists!" %int(zid)
                    continue
                
                # construct zone with zone id num, and filename
                tzone = zone.zone( zid, filename)
                
                # update zone dict
                hub.zones.update( {zid:tzone})


        


if __name__ == "__main__":
    hubinittest()
