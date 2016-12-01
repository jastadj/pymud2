import worldobject
import json
import hub
import copy

class iteminstance(worldobject.worldobjectinstance):
    
    def __init__(self, uidref, jobj = None):
        
        # init base class data
        worldobject.worldobjectinstance.__init__(self, uidref, jobj)
        
        self.idata = {"stack":1}
        
        if self.getref().iscontainer():
            self.container = self.getref().container.createpersistentdata()
        
        if jobj != None:
            self.fromJSON(jobj)
    
    def getnameex(self):
        
        return worldobject.worldobjectinstance.getnameex(self, self.getstack())
    
    def getlookstr(self):
        
        lookstr = worldobject.worldobjectinstance.getlookstr(self)
        
        if self.getref().iscontainer():
            citems = self.container.getitems()
            
            if len(citems) == 0:
                lookstr += "It contains nothing.\n"
            else:
                lookstr += "It Contains:\n"
                
                for i in citems:
                    lookstr += "  %s\n" %i.getnameex()
                    
            
        return lookstr
    
    def getstack(self):
        return self.idata["stack"]
        
    def setstack(self, stackval):
        if self.getref().isstackable():
            self.idata["stack"] = stackval
    
    def split(self, quantity):
        
        # if item is not stackable
        if not self.getref().isstackable():
            return None
        
        #debug
        print "splitting stack %d / %d from %s" %(quantity, self.getstack(), self.getnameex())
        
        # invalid quantity for stack
        if quantity < 1 or quantity >= self.getstack():
            return None
        
        # create new item and subttrack stack
        sitem = self.getref().create()
        sitem.setstack(quantity)
        
        self.setstack( self.getstack() - quantity)
        
        print "split new item quantity = %d, parent item quantity = %d" %(sitem.getstack(), self.getstack())
        
        return sitem
    
    def todict(self):
        tdict = worldobject.worldobjectinstance.todict(self)
        
        tdict.update( {"idata":self.idata} )
        
        if self.getref().iscontainer():
            tdict.update( {"container": self.container.todict() } )
        
        return tdict
    
    def fromJSON(self, jobj):
        
        self.idata = jobj["idata"]
        
        if self.getref().iscontainer():
            self.container.fromJSON(jobj["container"])
        
    def show(self):
        worldobject.worldobjectinstance.show(self)
        print "stack:%d" %self.getstack()
        
        if self.getref().iscontainer():
            self.container.show()


class sign(object):
    def __init__(self):
        self.sign = {"sign":""}
        
    def settext(self, signtext):
        self.sign["sign"] = signtext
    
    def gettext(self):
        return self.sign["sign"]
    
    def todict(self):
        tdict = {"sign":self.gettext() }
        return tdict
        
    def fromJSON(self, jobj):
        self.sign["sign"] = jobj["sign"]
    
    def show(self):
        print "sign!"

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
            return None
            
        # check if there is a stackable item already in container
        for i in self.inventory:
            if i.getref().getuid() == titem.getref().getuid():
                if i.getref().isstackable():
                    
                    print "ADDING ITEM, MERGING INTO STACK"
                    
                    # get stack count of item to merge
                    titemcount = titem.getstack()
                    
                    # merge item stack count with base item
                    i.setstack( i.getstack() + titemcount)
                    
                    # delete item from instances since it merged
                    hub.removeworldinstanceobject(titem)
                    
                    return i
        
        # else, not stackable, add to list
        self.inventory.append(titem)
        return titem
    
    def removeitem(self, titem, quantity = 1):
        if titem == None: return None
        if titem in self.inventory:
            
            # if item is stackable
            if titem.getref().isstackable():
                
                # if stackable item == specified quantity
                if titem.getstack() == quantity:
                    self.inventory.remove(titem)
                    return titem
                
                # if stackable item has enough to split
                if titem.getstack() > quantity:
                    
                    # split the stack
                    ritem = titem.split(quantity)
                    return ritem
                
                # else, cannot split
                return None
            
            # else if item is not stackable, remove and return
            self.inventory.remove(titem)
            return titem

        return None

    def deleteitem(self, titem):
        if self.removeitem(titem):
            return hub.removeworldinstanceobject(titem)
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
            self.additem(newitem)

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
        self.data = {"stackable":False, "static":False, "unlisted":False}
        
        # optional item structs
        self.weapon = None
        self.container = None
        self.food = None
        self.drink = None
        self.sign = None
        
        if jobj != None:
            self.fromJSON(jobj)

    def isitem(self):
        return True
    
    def isunlisted(self):
        return self.data["unlisted"]
    
    def isstatic(self):
        return self.data["static"]
    
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
        
    def issign(self):
        if self.sign != None:
            return True
        else: return False
    
    def setunlisted(self, unlisted):
        self.data["unlisted"] = unlisted
    
    def setstatic(self, static):
        self.data["static"] = static
    
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
        
    def makesign(self):
        self.sign = sign()
    
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
            
        if self.issign():
            tdict.update( {"sign":self.sign.todict() } )
        
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
            
        if "sign" in jobj.keys():
            self.sign = sign()
            self.sign.fromJSON( jobj["sign"])
        
    def create(self):
        newinstance = iteminstance(self.uid)
        
        return newinstance
    
    def show(self):
        worldobject.worldobject.show(self)
        print "isstackable:%s" %self.isstackable()
        print "isstatic:%s" %self.isstatic()
        print "isunlisted:%s" %self.isunlisted()
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
        print "issign:%s" %self.issign()
        
if __name__ == "__main__":
    
    dotest = 2
    
    if dotest == 1:
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
    
    if dotest == 2:
        print "ITEM 1 SIGN:\n"
        item1 = item("sign")
        item1.makesign()
        item1.sign.settext("THIS IS A SIGN!\n")
        item1.show()
        print item1.sign.gettext()
        jstrings = item1.toJSONstr()
        
        item1copy = item("test", json.loads(jstrings))
        
