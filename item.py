import worldobject
import json
import hub

class iteminstance(worldobject.worldobjectinstance):
    
    def __init__(self, uidref, jobj = None):
        
        # init base class data
        worldobject.worldobjectinstance.__init__(self, uidref, jobj)
        
    def show(self):
        worldobject.worldobjectinstance.show(self)


class item(worldobject.worldobject):
        
    def __init__(self, name = "unnamed", jobj = None):
        
        # init baseclass
        worldobject.worldobject.__init__(self, name, jobj)
        
        # init class data
        self.data = {}
        
        if jobj != None:
            self.fromJSON(jobj)

    
    def todict(self):
        tdict = worldobject.worldobject.todict(self)
        
        tdict.update( {"data":self.data} )
        
        return tdict
    
    def fromJSON(self, jobj):
        
        self.data = jobj["data"]
    
    def create(self):
        newinstance = iteminstance(self.uid)
        
        return newinstance
    
    def show(self):
        worldobject.worldobject.show(self)
        
if __name__ == "__main__":
    
    print "\nItem 1:"
    item1 = item("rock")
    item1.show()

    itemi = item1.create()
    itemi.show()
