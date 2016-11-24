import json
import worldobject
import hub
import copy
       

class room(worldobject.worldobject):
    def __init__(self, zoneid, roomid, name = "unnamed", jobj = None):
        
        # init baseclass
        worldobject.worldobject.__init__(self, name, jobj)

        # init class data
        self.data = {"zid":zoneid, "rid":roomid, "exits":{} }
        self.inventory = []

        # if json obj provided, load in data
        if jobj != None:
            room.fromJSON(self,jobj)
        
    def getzoneid(self):
        return self.data["zid"]
    
    def getroomid(self):
        return self.data["rid"]

    def getexits(self):
        return self.data["exits"]

    def addexit(self, exitname, exitroomnum):
        self.data["exits"].update( {exitname:exitroomnum} )

    def newitem(self, iuid):
        
        self.inventory.append(hub.ITEM(iuid))

    def getinventory(self):
        return self.inventory

    def todict(self):
        
        tdict = worldobject.worldobject.todict(self)
        
        # room data
        tdict.update( {"data":self.data} )
        
        return tdict

    def fromJSON(self, jobj):
        
        # base class json load
        # not necessary since this is done in constructor
        #worldobject.worldobject.fromJSON(self, jobj)
        
        # room data
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
        print "Inventory:"
        for i in self.inventory:
            print "  iid:%d (%d)" %(i.getiid(), i.getrefuid())

if __name__ == "__main__":
    
    room1 = room(0, 0, "Living Room")
    room1.setdescription("A pretty standard clean living room.")
    
    room1str = room1.toJSONstr()
    
    room1copy = room(1,1,"test", json.loads(room1str) )
    
    print "room1 json str:"
    print room1str
    
    print "\nroom1:"
    room1.show()
    
    print "\nroom1 copy:"
    room1copy.show()
    
    
