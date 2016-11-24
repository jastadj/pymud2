import json
import worldobject
import hub
import copy

import item

class room(worldobject.worldobject):
    def __init__(self, zoneid, roomid, name = "unnamed", jobj = None):
        
        # init baseclass
        worldobject.worldobject.__init__(self, name, jobj)

        # init class data
        self.data = {"zid":zoneid, "rid":roomid, "exits":{} }
        self.items = []

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

    def additem(self,titem):
        self.items.append(titem)
    
    def removeitem(self, titem):
        try:
            self.items.remove(titem)
            return True
        except:
            return False
        
    def getitems(self):
        return self.items

    def todict(self):
        
        tdict = worldobject.worldobject.todict(self)
        
        # room data
        tdict.update( {"data":self.data} )
        
        # inventory
        tdict.update( {"items":[] })
        for i in self.items:
            tdict["items"].append( i.todict() )
        
        return tdict

    def fromJSON(self, jobj):
        
        # base class json load
        # not necessary since this is done in constructor
        #worldobject.worldobject.fromJSON(self, jobj)
        
        # room data
        self.data = jobj["data"]
        
        # add items
        for i in jobj["items"]:
            newi = item.iteminstance(0, i)
            self.items.append(newi)
        

    def show(self):
        worldobject.worldobject.show(self)
        for d in self.data.keys():
            print "%s:%s" %(d, self.data[d])

        print "Items:"
        for i in self.items:
            print "  iid:%d / refid(%d) : %s" %(i.getiid(), i.getuidref(), i.getrefname())

if __name__ == "__main__":
    import item
    
    item1 = item.item("rock")
    item2 = item.item("book")
    item1i = item1.create()
    item2i = item2.create()
    
    
    
    room1 = room(0, 0, "Living Room")
    room1.setdescription("A pretty standard clean living room.")
    room1.additem(item1i)
    room1.additem(item2i)
    room1str = room1.toJSONstr()
    
    room1copy = room(1,1,"test", json.loads(room1str) )
    
    print "room1 json str:"
    print room1str
    
    print "\nroom1:"
    room1.show()
    
    print "\nroom1 copy:"
    room1copy.show()
    
    
