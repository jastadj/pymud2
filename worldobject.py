import noun
import hub
import json

class worldobject(noun.noun):
    
    # uidnum of 0 is reserved for all players
    uidcount = 1
    
    def __init__(self, name = "unnamed", jstr = None):
        noun.noun.__init__(self, name)

        # if type is character, uid 0 is reserved
        if self.gettype() == "character":
            self.uid = 0
            return

        # if no json string provided, assume new item
        if jstr == None:
            self.uid = worldobject.uidcount
            worldobject.uidcount += 1
        else:
            self.fromJSON(jstr)
        
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

    def toJSON(self):
        return json.dumps(self.__dict__)
        
    def fromJSON(self, jsonstring):
        jobj = json.loads(jsonstring)
        
        self.uid = jobj["uid"]
        self.name = jobj["name"]
        self.description = jobj["description"]
        self.article = jobj["article"]
        self.adjectives = jobj["adjectives"]
        self.verb = jobj["verb"]
        self.proper = jobj["proper"]

if __name__ == "__main__":
    
    myobjs = []
    
    mywords = ["dog", "car", "table", "rifle", "stick"]
    
    for o in range(0, 5):
        myobjs.append( worldobject(mywords[o]))
        myobjs[o].show()
    
    myobjs[0].addadjective("mangy")
    myobjs[0].setverb(" is sitting here patiently")
    myjstr = myobjs[0].toJSON()
    
    print myjstr
    
    testobj = worldobject("unnamed", myjstr)
    
    testobj.show()
