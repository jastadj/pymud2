import json
import copy
import worldobject
import hub


class item(object):
    
    iidcount = 0
    
    def __init__(self, itemrefid, jstr = None):
        
        if jstr == None:
            self.data = {"iid":item.iidcount, "refuid":itemrefid}
            item.iidcount += 1
        
        else:
            self.fromJSON(jstr)
        
        hub.worldobjects_instance.update( {self.data["iid"]:self} )
    
    def getiid(self):
        return self.data["iid"]
        
    def getrefuid(self):
        return self.data["refuid"]
    
    def show(self):
        print "item instance:"
        print "--------------"
        print "instance id = %d" %self.data["iid"]
        print "item ref id = %d" %self.data["refuid"]
        print "item ref name = %s" %hub.worldobjects[ self.data["refuid"] ].getname()
    
    def fromJSON(self, jstr):
        
        tobj = json.loads(jstr)
        self.data = tobj["data"]
    
    def makeserializable(self):
        
        tdict = {"data":self.data}
        
        return tdict
        

class weapon(object):
    def __init__(self):
        self.data = {"damage":1}
    
    def getdamage(self):
        return self.data["damage"]
    
    def setdamage(self, dmg):
        self.data["damage"] = dmg
        
    def makeserializable(self):
        tdict = self.data
        
        return tdict

class inventory(object):
    def __init__(self):
        self.inventory = []
    
    def makeserializable(self):
        
        tempinv = []
        
        for i in self.inventory:
            tempinv.append( i.makeserializable())

        tdict = dict({"inventory":tempinv})
        
        return tdict

class itemmaster(worldobject.worldobject):
        
    def __init__(self, name = "unnamed", savetocommon = True, jstr = None):
        worldobject.worldobject.__init__(self, name, jstr)
        
        # save to common add to the common items list
        # during item save, any item in this list will
        # be saved to the common items file
        # this allows for unique zone items to be kept
        # with the zone and not part of the common item
        # package
        if savetocommon:
            hub.commonitems.append(self)
        
        self.data = {}
        
        self.inventory = None
        self.weapon = None
    
        if jstr != None:
            self.fromJSON(jstr)
    
    def isweapon(self):
        if self.weapon != None: return True
        return False
        
    def iscontainer(self):
        if self.inventory != None: return True
        return False
    
    def makeserializable(self):
        tdict = copy.deepcopy(self.__dict__)
        
        # pop sub classes
        #tdict.pop("weapon", None)
        #tdict.pop("inventory", None)
        
        # if is a weapon
        if self.weapon != None:
            tdict.update( {"weapon": self.weapon.makeserializable() } )
        
        if self.inventory != None:
            tdict.update( {"inventory":self.inventory.makeserializable() } )
        
        return tdict
    
    def toJSON(self):
        
        return json.dumps(self.makeserializable())
    
    def fromJSON(self, jstr):
        
        jobj = json.loads(jstr)
        
        for k in jobj.keys():
            print "%s:%s" %(k, jobj[k])
            
    
    def show(self):
        worldobject.worldobject.show(self)
        print "is weapon:%s" %self.isweapon()
        if self.isweapon():
            print "  weapon damage:%d" %self.weapon.getdamage()
        print "is container:%s" %self.iscontainer()
        

        
    def create(self):
        return item(self.getuid())

if __name__ == "__main__":
    import hubinit
    
    hubinit.hubinittest()
    
    print "\nITEM TESTING\n"
    testitem1 = itemmaster("axe")
    testitem1.weapon = weapon()
    testitem1.weapon.setdamage(9)
    #testitem1.show()
    
    jstrings = testitem1.toJSON()
    print jstrings
    
    
