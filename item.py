import worldobject
import json
import hub
import copy

class iteminstance(worldobject.worldobjectinstance):
    
    def __init__(self, uidref, jobj = None):
        
        # init base class data
        worldobject.worldobjectinstance.__init__(self, uidref, jobj)
        
        self.data.update( {"stack":1} )
        
        if self.getref().iscontainer():
            self.container = self.getref().container.createpersistentdata()
        
        if jobj != None:
            self.fromJSON(jobj)
    
    def getlookstr(self):
        
        lookstr = worldobject.worldobjectinstance.getlookstr(self)
        
        if self.getref().iscontainer():
            citems = self.container.getitems()
            
            if len(citems) == 0:
                lookstr += "It contains nothing.\n"
            else:
                lookstr += "It Contains:\n"
                
                for i in citems:
                    lookstr += "  %s\n" %i.getref().getnameex()
                    
            
        return lookstr
        
    def todict(self):
        tdict = worldobject.worldobjectinstance.todict(self)
        
        if self.getref().iscontainer():
            tdict.update( {"container": self.container.todict() } )
        
        return tdict
    
    def fromJSON(self, jobj):
        
        if self.getref().iscontainer():
            self.container.fromJSON(jobj["container"])
        
    def show(self):
        worldobject.worldobjectinstance.show(self)
        
        if self.getref().iscontainer():
            self.container.show()



class drink(object):
    def __init__(self):
        pass
    
    def todict(self):
        pass
    
    def fromJSON(self, jobj):
        pass
    
    def show(self):
        pass   

class food(object):
    def __init__(self):
        pass
    
    def todict(self):
        pass
    
    def fromJSON(self, jobj):
        pass
    
    def show(self):
        pass

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

class pcontainer(object):
    def __init__(self):
        self.inventory = []
    
    def getitems(self):
        return self.inventory
    
    def additem(self, titem):
        if titem == None:
            return False
        self.inventory.append(titem)
        return True
    
    def removeitem(self, titem):
        if titem == None: return False
        if titem in self.inventory:
            self.inventory.remove(titem)
            return True
        return False

    def todict(self):
        
        tdict = {}
        
        tdict.update( {"items":[]} )
        
        for i in self.inventory:
            tdict["items"].append( i.todict() )
        
        return tdict
    
    def fromJSON(self, jobj):
        
        for i in jobj["items"]:          
            newitem = iteminstance(0, i)
            self.inventory.append(newitem)

    def show(self):
        print "Items:"
        for i in self.inventory:
            print "  iid:%d / refid(%d) : %s" %(i.getiid(), i.getuidref(), i.getnameex())

class pcorpse(pcontainer):
    def __init__(self):
        pcontainer.__init__(self)
    
    def todict(self):
        tdict = pcontainer.todict(self)
        
        return tdict
    
    def fromJSON(self, jobj):
        pcontainer.fromJSON(self, jobj)
    
    def show(self):
        pcontainer.show(self)
    

class container(object):
    def __init__(self):
        self.container = {"maxweight":0, "maxvolume":0}

    def createpersistentdata(self):
        return pcontainer()
        
    def getmaxweight(self):
        return self.container["maxweight"]
    
    def getmaxvolume(self):
        return self.container["maxvolume"]
        
    def setmaxweight(self, weight):
        self.container["maxwieght"] = weight
    
    def setmaxvolume(self, volume):
        self.container["maxvolume"] = volume

    def todict(self):
        
        tdict = {}
        
        tdict.update( {"container": self.container} )
        
        return tdict
    
    def fromJSON(self, jobj):
        
        self.container = jobj["container"]

    def show(self):
        print "Container Data:"
        for d in self.container.keys():
            print "  %s:%s" %(d, self.container[d])   

class corpse(container):
    def __init__(self):
        container.__init__(self)
    
    def createpersistentdata(self):
        return pcorpse()
    
    def todict(self):
        
        tdict = {}
        
        tdict.update( {"corpse": self.container} )
        
        return tdict
    
    def fromJSON(self, jobj):
        
        self.container = jobj["corpse"]

    def show(self):
        print "Corpse Data:"
        for d in self.container.keys():
            print "  %s:%s" %(d, self.container[d]) 

class item(worldobject.worldobject):
        
    def __init__(self, name = "unnamed", jobj = None):
        
        # init baseclass
        worldobject.worldobject.__init__(self, name, jobj)
        
        # init class data
        self.data = {"stackable":False}
        
        # optional item structs
        self.weapon = None
        self.container = None
        self.food = None
        self.drink = None
        
        if jobj != None:
            self.fromJSON(jobj)

    def isitem(self):
        return True
    
    def isstackable(self):
        return self.data["stackable"]
    
    def isweapon(self):
        if self.weapon != None:
            return True
        else: return False
    
    def iscontainer(self):
        if self.container != None:
            return True
        else: return False
    
    def iscorpse(self):
        if self.container.__class__.__name__ == "corpse":
            return True
        else: return False
    
    def isfood(self):
        if self.food != None:
            return True
        else: return False
    
    def isdrink(self):
        if self.drink != None:
            return True
        else: return False
    
    def setstackable(self, stackable):
        self.data["stackable"] = stackable
    
    def makeweapon(self):
        self.weapon = weapon()
    
    def makecontainer(self):
        self.container = container()
    
    def makefood(self):
        self.food = food()
    
    def makedrink(self):
        self.drink = drink()
    
    def makecorpse(self):
        self.container = corpse()
    
    def todict(self):
        tdict = worldobject.worldobject.todict(self)
        
        tdict.update( {"data":self.data} )
        
        if self.isweapon():
            tdict.update( {"weapon":self.weapon.todict()} )
        
        if self.iscontainer():
            if self.container.__class__.__name__ == "container":
                tdict.update( {"container":self.container.todict() } )
            elif self.iscorpse():
                tdict.update( {"corpse":self.container.todict() } )
        
        if self.isfood():
            tdict.update( {"food":self.food.todict() } )
        
        if self.isdrink():
            tdict.update( {"drink":self.drink.todict() } )
        
        return tdict
    
    def fromJSON(self, jobj):
        
        self.data = jobj["data"]
        
        if "weapon" in jobj.keys():
            self.weapon = weapon()
            self.weapon.fromJSON( jobj["weapon"])
    
        if "container" in jobj.keys():
            self.container = container()
            self.container.fromJSON( jobj["container"])
        if "corpse" in jobj.keys():
            self.container = corpse()
            self.container.fromJSON( jobj["corpse"])
    
        if "food" in jobj.keys():
            self.food = food()
            self.food.fromJSON( jobj["food"])
        
        if "drink" in jobj.keys():
            self.drink = drink()
            self.drink.fromJSON( jobj["drink"])
        
    def create(self):
        newinstance = iteminstance(self.uid)
        
        return newinstance
    
    def show(self):
        worldobject.worldobject.show(self)
        print "isstackable:%s" %self.isstackable()
        print "isweapon:%s" %self.isweapon()
        if self.isweapon():
            self.weapon.show()
        print "iscontainer:%s" %self.iscontainer()
        if self.iscontainer():
            self.container.show()
        print "isfood:%s" %self.isfood()
        if self.isfood():
            self.food.show()
        print "isdrink:%s" %self.isdrink()
        if self.isdrink():
            self.drink.show()
        
if __name__ == "__main__":
    
    print "\nItem 1:"
    item1 = item("dagger")
    item1.makeweapon()
    item1.show()

    print "\nItem 2:"
    item2 = item("sack")
    item2.makecontainer()
    item2.show()

    print "\nItem 1 Instance:"
    item1i = item1.create()
    item1i.show()

    print "\nItem 2 Instance:"
    item2i = item2.create()
    item2i.container.additem(item1i)
    item2i.show()
    
    jstrings = item2i.toJSONstr()
    print "\nItem 2 Instance Copy"
    item2icopy = iteminstance(0, json.loads(jstrings) )
    item2icopy.show()
