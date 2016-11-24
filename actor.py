import json
import worldobject
import item

class actorinstance(worldobject.worldobjectinstance):
    
    def __init__(self, uidref, jobj = None):
        
        # init base class data
        worldobject.worldobjectinstance.__init__(self, uidref, jobj)
    
    def show(self):
        worldobject.worldobjectinstance.show(self)

class actor(worldobject.worldobject):
    def __init__(self, name = "unnamed", jobj = None):
        
        # init base class data        
        worldobject.worldobject.__init__(self, name, jobj)
        
        # init class data
        self.data = {}
        #self.inventory = []
        
        # if json object supplied, load from that
        if jobj != None:
            self.fromJSON(jobj)
    
    def todict(self):
        
        tdict = worldobject.worldobject.todict(self)
        
        tdict.update( {"data":self.data} )
        
        """
        tdict.update( {"inventory":[]} )
        for i in self.inventory:
            tdict["inventory"].append( i.todict() )
        """
        
        return tdict
    
    def fromJSON(self, jobj):
        
        self.data = jobj["data"]
        
        """
        for k in jobj["inventory"]:
            newi = item.iteminstance(0, k)
            self.inventory.append(newi)
        """
    def show(self):
        worldobject.worldobject.show(self)
        
        """
        print "Inventory:"
        for i in self.inventory:
            print "  iid:%d / refid(%d) : %s" %(i.getiid(), i.getuidref(), i.getrefname())
        """
        
if __name__ == "__main__":
    
    actor1 = actor("dog")
    
    actor1.show()
