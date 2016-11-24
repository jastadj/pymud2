import noun
import hub
import json

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
