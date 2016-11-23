import json
import worldobject
import hub
       

class room(worldobject.worldobject):
    def __init__(self, zoneid, roomid, name = "unnamed", jstr = None):
        worldobject.worldobject.__init__(self, name, jstr)
                
        self.data = {"zid":zoneid, "rid":roomid, "exits":{} }

        # if json strings provided
        if jstr != None:
            self.fromJSON(jstr)
        
    def getzoneid(self):
        return self.data["zid"]
    
    def getroomid(self):
        return self.data["rid"]

    def getexits(self):
        return self.data["exits"]

    def addexit(self, exitname, exitroomnum):
        self.data["exits"].update( {exitname:exitroomnum} )

    def fromJSON(self, jsonstring):
        
        # base class json load
        worldobject.worldobject.fromJSON(self, jsonstring)
        
        # room data json load
        jobj = json.loads(jsonstring)
        self.data = jobj["data"]

    def show(self):
        worldobject.worldobject.show(self)
        for d in self.data.keys():
            print "%s:%s" %(d, self.data[d])
        if len(self.getexits().keys()) == 0:
            print "No exits."
        else:
            print "Exits:"
            for e in self.getexits().keys():
                print "  %s:%d" %(e, self.getexits()[e])

if __name__ == "__main__":
    pass
    
