import noun
import hub
import json

class objectspawner(object):
    def __init__(self, troom = None, tobj = None, maxticks = 60):
        
        # if no room or object supplied
        if troom == None or tobj == None:
            self.data = {"roomuid":troom, "objuid":tobj}
        # else, either use uid or object
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
            self.data = {"roomuid":troom.getuid(), "objuid":tobj.getuid()}
        
        # additional data
        self.data.update( {"ticks":0, "maxticks":maxticks, "lastinstance":None, "maxcount":None} )
        self.data.update( {"stack":1} )
        
        # temporary data
        self.count = 0
        
        
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
    
    def getstack(self):
        return self.data["stack"]
    
    def getcount(self):
        return self.count
        
    def getmaxcount(self):
        return self.data["maxcount"]
    
    def maxcountreached(self):
        if self.getmaxcount() != None:
            if self.getcount() >= self.getmaxcount():
                return True
        return False
    
    def setmaxticks(self, maxticks):
        self.data["maxticks"] = maxticks
        
    def setticks(self, ticks):
        self.data["ticks"] = ticks
    
    def setmaxcount(self, maxcount):
        self.data["maxcount"] = maxcount
        
    def setstack(self, stack):
        if self.getref().isitem():
            if self.getref().isstackable():
                self.data["stack"] = stack
    
    def dotick(self):
        self.data["ticks"] += 1
        if self.data["ticks"] >= self.data["maxticks"]:
            self.data["ticks"] = 0
            
            #if max count reached, do nothing
            #this should be cleaned up also by parent, removing the spawner
            #once max count has been reached
            
            if self.maxcountreached():
                return False
            
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
                
                # if stackable, set stack size from spawner
                if newobj.getref().isstackable():
                    newobj.setstack( self.data["stack"] )
                
                # add object to room
                newobj = troom.additem(newobj)

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

            #increment spawn counter
            self.count += 1

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
        
        hub.worldobjinstancemutex.acquire()
        
        try:
            # init persistent item data
            self.data = {"uidref":uidref}
            
            self.iid = worldobjectinstance.iidcount
            # increase iid counter
            worldobjectinstance.iidcount += 1

            # register instance object
            hub.addworldinstanceobject(self)

            if jobj != None:
                worldobjectinstance.fromJSON(self,jobj)
        finally:
            hub.worldobjinstancemutex.release()

    def dotick(self):
        pass

    def initcustomnoun(self):
        
        # get json object of reference noun
        noundict = noun.noun.todict( self.getref() )
        nounjstr = json.dumps(noundict)
        nounjobj = json.loads( nounjstr)
        
        # create copy of noun
        cnoun = noun.noun("unnamed")
        cnoun.fromJSON( nounjobj)
        
        # set persistent data custom noun
        self.data.update( {"customnoun": cnoun} )

    def getcustomnoun(self):
        
        if "customnoun" in self.data.keys():
            return self.data["customnoun"]

    def gettype(self):
        return self.__class__.__name__

    def getuidref(self):
        return self.data["uidref"]
    
    def getiid(self):
        return self.iid
    
    def getref(self):
        return hub.worldobjects[ self.data["uidref"] ]
        
    def getnameex(self, plural = False, showverb = False):
        if "customnoun" in self.data.keys():
            return self.data["customnoun"].getnameex(plural, showverb)
        else:
            return self.getref().getnameex(plural, showverb)

    def getnoun(self):
        if "customnoun" in self.data.keys():
            return self.data["customnoun"]
        else:
            return self.getref()

    def getlookstr(self):
        return self.getref().getdescription() + "\n"
    
    def todict(self):
        tdict = {}
        
        # pop custom noun
        cnoun = self.data.pop("customnoun", None)
        
        tdict.update( {"data":self.data } )
        
        # if custom noun, add dict
        if cnoun != None:
            tdict.update( {"customnoun":cnoun.todict() } )
        
        return tdict
        
    def toJSONstr(self):
        return json.dumps( self.todict() )
        
    def fromJSON(self, jobj):
        
        self.data = jobj["data"]
        
        # if custom noun
        if "customnoun" in self.data.keys():
            cnoun = noun.noun()
            cnoun.fromJSON( self.data["customnoun"] )
            self.data["customnoun"] = cnoun
    
    def show(self):
        print "item instance:"
        print "--------------"
        print "iid:%d" %self.iid
        print "uid ref:%d" %self.data["uidref"]
        print "ref name:%s" %hub.worldobjects[self.data["uidref"]].getnameex()
        if "customnoun" in self.data.keys():
            print "Custom Noun:%s" % self.data["customnoun"].getnameex()
        

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
        
        tdict = noun.noun.todict(self)
        
        tdict.update( {"uid":self.uid} )
        
        
        return tdict
        
    def toJSONstr(self):
        return json.dumps( self.todict() )
        
    def fromJSON(self, jobj):
        
        noun.noun.fromJSON(self, jobj)
        
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
