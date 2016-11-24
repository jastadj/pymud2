import worldobject
import json
import hub

class iteminstance(worldobject.worldobjectinstance):
    
    def __init__(self, uidref, jobj = None):
        
        # init base class data
        worldobject.worldobjectinstance.__init__(self, uidref, jobj)
        
    def show(self):
        worldobject.worldobjectinstance.show(self)

class weapon(object):
    def __init__(self):
        self.weapon = {"damage":1}
    
    def getdamage(self):
        return self.weapon["damage"]
    
    def setdamage(self, val):
        self.weapon["damage"] = val
    
    def todict(self):
        return self.weapon
        
    def fromJSON(self, jobj):
        self.weapon = jobj
    
    def show(self):
        print "Weapon:"
        for d in self.weapon.keys():
            print "  %s:%s" %(d, self.weapon[d])

class item(worldobject.worldobject):
        
    def __init__(self, name = "unnamed", jobj = None):
        
        # init baseclass
        worldobject.worldobject.__init__(self, name, jobj)
        
        # init class data
        self.data = {}
        
        # optional item structs
        self.weapon = None
        
        if jobj != None:
            self.fromJSON(jobj)

    def isweapon(self):
        if self.weapon != None:
            return True
        else: return False
    
    def makeweapon(self):
        self.weapon = weapon()
    
    def todict(self):
        tdict = worldobject.worldobject.todict(self)
        
        tdict.update( {"data":self.data} )
        
        if self.isweapon():
            tdict.update( {"weapon":self.weapon.todict()} )
        
        return tdict
    
    def fromJSON(self, jobj):
        
        self.data = jobj["data"]
        
        if "weapon" in jobj.keys():
            self.weapon = weapon()
            self.weapon.fromJSON( jobj["weapon"])
    
    def create(self):
        newinstance = iteminstance(self.uid)
        
        return newinstance
    
    def show(self):
        worldobject.worldobject.show(self)
        print "isweapon:%s" %self.isweapon()
        if self.isweapon():
            self.weapon.show()
        
if __name__ == "__main__":
    
    print "\nItem 1:"
    item1 = item("dagger")
    item1.makeweapon()
    item1.show()

    itemi = item1.create()
    itemi.show()
