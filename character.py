import json
import actor
import worldobject
import defs
import hub
from tools import *

import item

class character(actor.actor, actor.actorinstancedata):
    def __init__(self, user, name = "unnamed"):
        
        if user.getcharacterfile() == None:
            print "Error creating character, character file is none!"
        
        # init base class data
        actor.actor.__init__(self, name)
        actor.actorinstancedata.__init__(self, self)
        
        self.setproper(True)
        
        self.data.update( {"owner":user.getuser()} )
        
        self.client = None
        
        fp = defs.CHARACTERS_PATH + user.getcharacterfile()
        
        # character file exists
        if createNewFile(fp) == None:
            
            with open(fp, "r") as f:
                
                for line in f:
                    
                    line = line[:-1]
                    
                    self.fromJSON( json.loads(line) )
                    
            f.close()

    def setclient(self, tclient):
        self.client = tclient
        
    def getclient(self):
        return self.client

    
    def todict(self):
        
        # get base class data
        tdict = actor.actor.todict(self)
        
        tdict.update( actor.actorinstancedata.todict(self) )
        
        # get class data
        tdict.update( {"data":self.data} )
        
        return tdict
    
    def fromJSON(self, jobj):
        
        # get base class data
        worldobject.worldobject.fromJSON(self, jobj)
        actor.actor.fromJSON(self, jobj)
        actor.actorinstancedata.fromJSON(self, jobj)
        
        # get class data
        self.data = jobj["data"]
        
        
    
    def show(self):
        
        actor.actor.show(self)
        actor.actorinstancedata.show(self)
        
    def save(self):
        
        user = hub.accounts.accounts[ self.data["owner"] ]
        cfile = user.getcharacterfile()
        
        if cfile == None: return False
        
        fp = defs.CHARACTERS_PATH + cfile
        
        # character file exists
        createNewFile(fp)
        
        f = open(fp, "w")
        
        f.write( self.toJSONstr() + "\n")
        
        f.close()
        
if __name__ == "__main__":
    
    import hubinit
    import hub
    hubinit.hubinittest()
    
    hub.accounts.add("test","test")
    taccount = hub.accounts.dologin("test","test")
    taccount.data["characterfile"] = "testchar.dat"
    
    mychar = character(taccount, "Billy")
    mychar.show()
