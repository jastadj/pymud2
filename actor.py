import json
import worldobject
import item
import copy

class actor(worldobject.worldobject):
    def __init__(self, name = "unnamed", jobj = None):
        
        # init base class data        
        worldobject.worldobject.__init__(self, name, jobj)
        
        # init class data
        self.data = {}
        self.attributes = {}
        
        # config attributes
        self.attributes.update( {"hp":1})
        
        #self.inventory = []
        
        # if json object supplied, load from that
        if jobj != None:
            self.fromJSON(jobj)
    
    def isactor(self):
        return True
    
    def isinstance(self):
        return issubclass(self.__class__, actorinstancedata)
    
    def getattribute(self, attribute):
        if attribute in self.attributes.keys():
            return self.attributes[attribute]
        else:
            # try to get actor instance attribute
            ap = actorinstancedata.getattribute(self, attribute)
            return ap
    
    def setattribute(self, attribute, val):
        if attribute in self.attributes.keys():
            self.attributes[attribute] = val
            return True
        else:
            return actorinstancedata.setattribute(self, attribute, val)
    
    def todict(self):
        
        tdict = worldobject.worldobject.todict(self)
        
        tdict.update( {"data":self.data} )
        
        tdict.update( {"attributes":self.attributes} )
        """
        tdict.update( {"inventory":[]} )
        for i in self.inventory:
            tdict["inventory"].append( i.todict() )
        """
        
        return tdict
    
    def fromJSON(self, jobj):
        
        self.data = jobj["data"]
        
        self.attributes = jobj["attributes"]
        
        """
        for k in jobj["inventory"]:
            newi = item.iteminstance(0, k)
            self.inventory.append(newi)
        """
    def show(self):
        worldobject.worldobject.show(self)
        print "isinstance:%s" %self.isinstance()
        print "Attributes:"
        for a in self.attributes:
            print "  %s:%s" %(a, self.attributes[a])
        """
        print "Inventory:"
        for i in self.inventory:
            print "  iid:%d / refid(%d) : %s" %(i.getiid(), i.getuidref(), i.getrefname())
        """
   
class actorinstancedata(object):
    
    def __init__(self, tactor):
        
        self.pattributes = {"currenthp": tactor.getattribute("hp")}

    def getattribute(self, attribute):
        if attribute in self.pattributes.keys():
            return self.pattributes[attribute]
        else:
            return None
    
    def setattribute(self, attribute, val):
        if attribute in self.pattributes.keys():
            self.pattributes[attribute] = val
            return True
        else:
            return False

    def isalive(self):
        if self.pattributes["currenthp"] <= 0:
            return False
        return True

    def todict(self):
        tdict = {}
        
        tdict.update( {"pattributes":self.pattributes } )
        
        return tdict
        
    def fromJSON(self, jobj):
        
        self.pattributes = jobj["pattributes"]
        
    def show(self):
        print "Persistent Attributes:"
        for p in self.pattributes.keys():
            print "  %s:%s" %(p, self.pattributes[p])

class mob(actor):
    def __init__(self, name = "unnamed", jobj = None):
        
        # init base class data
        actor.__init__(self, name, jobj)
        
        # init class data
        # note: data already is derived from actor, only update dict
        
        self.mobdata = {}
        
        if jobj != None:
            self.fromJSON(jobj)
        
    def todict(self):
        
        # get actor data
        tdict = actor.todict(self)
        
        # get mob data
        tdict.update( {"mobdata":{} } )
        
        return tdict
    
    def fromJSON(self, jobj):
        
        # get actor data
        actor.fromJSON(self, jobj)
        
        # get mob data
        self.mobdata = jobj["mobdata"]
        
    def show(self):
        # show from base class
        actor.show(self)
    
    def create(self):
        newi = mobinstance(self.uid)
        return newi

class mobinstance(worldobject.worldobjectinstance, actorinstancedata):
    
    def __init__(self, uidref, jobj = None):
        
        # init base class data
        worldobject.worldobjectinstance.__init__(self, uidref, jobj)
        actorinstancedata.__init__(self, self.getref())

    def todict(self):
        tdict = worldobject.worldobjectinstance.todict(self)
        
        tdict.update( actorinstancedata.todict(self) )
        
        return tdict
        
    def fromJSON(self, jobj):
        
        worldobject.worldobjectinstance.fromJSON(self, jobj)
        
        actorinstancedata.fromJSON(self, jobj)
    
    def show(self):
        worldobject.worldobjectinstance.show(self)
        actor.show(self)
        actorinstancedata.show(self)

     
if __name__ == "__main__":
    
    print "\nMob 1:"
    mob1 = mob("dog")
    mob1.setattribute("hp", 5)
    mob1.show()
    
    print "\nMob 1 Instance:"
    mob1i = mob1.create()
    mob1i.show()
