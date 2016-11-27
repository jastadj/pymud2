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
        
        self.data.update( {"owner":user.getuser(), "currentzone":0, "currentroom":0} )
        self.inventory = []
        
        
        fp = defs.CHARACTERS_PATH + user.getcharacterfile()
        
        # character file exists
        if createNewFile(fp) == None:
            
            with open(fp, "r") as f:
                
                for line in f:
                    
                    line = line[:-1]
                    
                    self.fromJSON( json.loads(line) )
                    
            f.close()
    
    def getcurrentzoneid(self):
        return self.data["currentzone"]
    
    def getcurrentroomid(self):
        return self.data["currentroom"]
        
    def setcurrentzoneid(self, zid):
        self.data["currentzone"] = zid
    
    def setcurrentroomid(self, rid):
        self.data["currentroom"] = rid
    
    def getinventory(self):
        return self.inventory
    
    def additem(self, titem):
        self.inventory.append(titem)
    
    def removeitem(self, titem):
        try:
            self.inventory.remove(titem)
            return True
        except:
            return False
    
    def todict(self):
        
        # get base class data
        tdict = actor.actor.todict(self)
        
        tdict.update( actor.actorinstancedata.todict(self) )
        
        # get class data
        tdict.update( {"data":self.data} )
        
        # get class inventory
        tdict.update( {"inventory":[]} )
        for i in self.inventory:
            tdict["inventory"].append( i.todict() )        
        
        return tdict
    
    def fromJSON(self, jobj):
        
        # get base class data
        worldobject.worldobject.fromJSON(self, jobj)
        actor.actor.fromJSON(self, jobj)
        actor.actorinstancedata.fromJSON(self, jobj)
        
        # get class data
        self.data = jobj["data"]
        
        # get class inventory
        for k in jobj["inventory"]:
            newi = item.iteminstance(0, k)
            self.inventory.append(newi)        
    
    def show(self):
        
        actor.actor.show(self)
        actor.actorinstancedata.show(self)
        
        print "Inventory:"
        for i in self.inventory:
            print "  iid:%d / refid(%d) : %s" %(i.getiid(), i.getuidref(), i.getrefname())        
        
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
