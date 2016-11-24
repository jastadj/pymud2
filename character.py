import json
import worldobject
import defs
import hub
from tools import *

class character(worldobject.worldobject):
    def __init__(self, user, name = "unnamed"):
        
        if user.getcharacterfile() == None:
            self = None
            return
        
        worldobject.worldobject.__init__(self, name)
        
        self.data = {"owner":user.getuser(), "currentzone":0, "currentroom":0}
        
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
    
    def todict(self):
        
        tdict = worldobject.worldobject.todict(self)
        
        tdict.update( {"data":self.data} )
        
        return tdict
    
    def fromJSON(self, jobj):
        
        worldobject.worldobject.fromJSON(self, jobj)
        
        self.data = jobj["data"]
        
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
        
        
