import noun
import hub
import json

class worldobjectinstance(object):
    # instance id counter
    iidcount = 0
    
    def __init__(self, uidref, jobj = None):
        
        # init persistent item data
        self.data = {"uidref":uidref, "iid":worldobjectinstance.iidcount}
        
        # update persistent item dictionary with instance id
        hub.worldobjects_instance.update( { self.data["iid"]: self} )
        
        # increate iid counter
        if jobj != None:
            worldobjectinstance.fromJSON(self, jobj)
        else:
            worldobjectinstance.iidcount += 1

    def gettype(self):
        return self.__class__.__name__

    def getuidref(self):
        return self.data["uidref"]
    
    def getiid(self):
        return self.data["iid"]
    
    def getref(self):
        return hub.worldobjects[ self.data["uidref"] ]
    
    def getrefname(self):
        return hub.worldobjects[ self.data["uidref"] ].getnameex()
    
    def todict(self):
        tdict = {}
        
        tdict.update( {"data":self.data } )
        
        return tdict
        
    def toJSONstr(self):
        return json.dumps( self.todict() )
        
    def fromJSON(self, jobj):
        
        self.data = jobj["data"]
    
    def show(self):
        print "item instance:"
        print "--------------"
        print "iid:%d" %self.data["iid"]
        print "uid ref:%d" %self.data["uidref"]
        print "ref name:%s" %hub.worldobjects[self.data["uidref"]].getnameex()
        

class worldobject(noun.noun):
    
    # uidnum of 0 is reserved for all players
    uidcount = 1
    
    def __init__(self, name = "unnamed", jobj = None):
        noun.noun.__init__(self, name)
        
        self.uid = worldobject.uidcount
        

        # if type is character, uid 0 is reserved
        if self.gettype() == "character":
            self.uid = 0
            return

        # if no json string provided, assume new item
        if jobj == None:
            worldobject.uidcount += 1
        else:
            worldobject.fromJSON(self, jobj)
        
        # register world object
        hub.addworldobject(self)
        
    def getuid(self):
        return self.uid
    
    def gettype(self):
        return self.__class__.__name__
    
    def show(self):
        print "object info:"
        print "------------"
        print "uid:%d" %self.uid
        print "type:%s" %self.gettype()
        print "name:%s" %self.getnameex()


    def todict(self):
        
        tdict = {}
        
        tdict.update( {"noundata":self.noundata} )
        tdict.update( {"uid":self.uid} )
        
        
        return tdict
        
    def toJSONstr(self):
        return json.dumps( self.todict() )
        
    def fromJSON(self, jobj):
        
        self.noundata = jobj["noundata"]
        self.uid = jobj["uid"]

if __name__ == "__main__":
    
    myobjs = []
    
    mywords = ["dog", "car", "table", "rifle", "stick"]
    
    for o in range(0, 5):
        myobjs.append( worldobject(mywords[o]))
        myobjs[o].show()
    
    myobjs[0].addadjective("mangy")
    myobjs[0].setverb(" is sitting here patiently")
    myjstr = myobjs[0].toJSONstr()
    
    print myjstr
    
    testobj = worldobject("unnamed", json.loads(myjstr) )
    
    testobj.show()
