import noun
import hub
import json

class objectspawner(object):
    def __init__(self, troom = None, tobj = None, maxticks = 60):
        
        if troom == None or tobj == None:
            self.data = {"roomuid":troom, "objuid":tobj, "ticks":0, "maxticks":maxticks}
            self.data.update( {"lastinstance":None} )
        else:
            if type(troom) == int:
                troom = hub.worldobjects[troom]
                if not troom.isroom():
                    troom = None
            if type(tobj) == int:
                tobj = hub.worldobjects[tobj]
                if not tobj.isitem():
                    if not tobj.isactor():
                        tobj = None
            self.data = {"roomuid":troom.getuid(), "objuid":tobj.getuid(), "ticks":0, "maxticks":maxticks}
    
    def getdata(self):
        return self.data
    
    def getroomuid(self):
        return self.data["roomuid"]
        
    def getobjuid(self):
        return self.data["objuid"]
        
    def getticks(self):
        return self.data["ticks"]
    
    def getmaxticks(self):
        return self.data["maxticks"]

    def getref(self):
        return hub.worldobjects[ self.data["objuid"] ]

    def getlastinstance(self):
        if self.data["lastinstance"] != None:
            try:
                return hub.worldobjects_instance[ self.data["lastinstance"] ]
            except:
                return None
        return None

    def setmaxticks(self, maxticks):
        self.data["maxticks"] = maxticks
        
    def setticks(self, ticks):
        self.data["ticks"] = ticks
        
    def dotick(self):
        self.data["ticks"] += 1
        if self.data["ticks"] >= self.data["maxticks"]:
            self.data["ticks"] = 0
            
            # get room for spawning
            troom = hub.worldobjects[ self.data["roomuid"] ]
            newobj = None
            
            #if target object is item
            if self.getref().isitem():
                
                # if last instance of item is in target room, do nothing
                if self.getlastinstance() != None:
                    for i in troom.getitems():
                        if i.getiid() == self.getlastinstance().getiid():
                            return

                # create object
                newobj = hub.createobject( self.data["objuid"] )
                
                # add object to room
                troom.additem(newobj)

            elif self.getref().isactor():
                
                # if last instance of is still alive, ignore
                if self.getlastinstance() != None:
                    if self.getlastinstance().isalive():
                        return
                
                # create object
                newobj = hub.createobject( self.data["objuid"] )
                
                # add actor to room
                troom.addmob(newobj)
            
            # set last instance reference to this new object
            self.data["lastinstance"] = newobj.getiid()

            # debug
            #print "Spawned %s" %newobj.getnameex()
            #print "Spawned %s" %self.getref().getnameex()
    
    def todict(self):
        
        tdict = {"data":self.data}
        
        return tdict
    
    def fromJSON(self, jobj):
        self.data = jobj["data"]
        self.data["lastinstance"] = None
    
    

class worldobjectinstance(object):
    # instance id counter
    iidcount = 0
    
    def __init__(self, uidref, jobj = None):
        
        # init persistent item data
        self.data = {"uidref":uidref}
        
        self.iid = worldobjectinstance.iidcount
        # increase iid counter
        worldobjectinstance.iidcount += 1

        # register instance object
        hub.addworldinstanceobject(self)

        if jobj != None:
            worldobjectinstance.fromJSON(self,jobj)

    def dotick(self):
        pass

    def gettype(self):
        return self.__class__.__name__

    def getuidref(self):
        return self.data["uidref"]
    
    def getiid(self):
        return self.iid
    
    def getref(self):
        return hub.worldobjects[ self.data["uidref"] ]
    
    def getrefname(self):
        return hub.worldobjects[ self.data["uidref"] ].getnameex()

    def getlookstr(self):
        return self.getref().getdescription() + "\n"
    
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
        print "iid:%d" %self.iid
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
    
    def isroom(self):
        return False
    def isitem(self):
        return False
    def isactor(self):
        return False
    
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
