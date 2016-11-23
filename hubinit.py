import defs
import timer
from tools import *
import account
import client
import testclient
import hub
import command

import zone

from tools import *

def hubinit():

    # clear lists
    hub.clients = []
    
    # load accounts
    hub.accounts = account.accountmanager()
    
    # load commands
    hub.cmds_main = command.initmaincommands()
    hub.cmds_main.setinvalidfunction( command.maingameinvalid )
        
    # timer
    hub.timer = timer.timer()
    print "Timer start:%f" %hub.timer.getstarttime()
    
    # load zones
    loadzones()


    # init summary
    print "Loaded %d zones." %len(hub.zones.keys())

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
        


if __name__ == "__main__":
    hubinittest()
