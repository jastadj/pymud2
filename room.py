import json
import worldobject
import hub
import copy

import item
import actor

class room(worldobject.worldobject):
    def __init__(self, zoneid, roomid, name = "unnamed", jobj = None):
        
        # init baseclass
        worldobject.worldobject.__init__(self, name, jobj)

        # init class data
        self.data = {"zid":zoneid, "rid":roomid, "exits":{} }
        self.data.update( {"descriptors":{}} )
        
        self.spawners = []
        #self.items = []
        self.items = item.pcontainer()
        self.mobs = []

        # if json obj provided, load in data
        if jobj != None:
            room.fromJSON(self,jobj)
    
    def dotick(self):
        
        self.dospawners()
        
        for i in self.getitems():
            i.dotick()
        
        for m in self.getmobs():
            m.dotick()
    
    def isroom(self):
        return True
    
    def getzoneid(self):
        return self.data["zid"]
    
    def getroomid(self):
        return self.data["rid"]

    def getexits(self):
        return self.data["exits"]

    def addexit(self, exitname, exitroomnum):
        self.data["exits"].update( {exitname:exitroomnum} )

    def adddescriptor(self, ddict):
        self.data["descriptors"].update( ddict )

    def getdescriptors(self):
        return self.data["descriptors"]


    #####
    # ITEMS
    
    def getitems(self):
        return self.items.getitems()
        
    def additem(self,titem):
        return self.items.additem(titem)
    
    def removeitem(self, titem):
        return self.items.removeitem(titem)

    
    def deleteitem(self, titem):
        return self.items.deleteitem(titem)

    #####
    # MOBS
    
    def getmobs(self):
        return self.mobs
    
    def addmob(self, tmob):
        if tmob != None:
            self.mobs.append(tmob)
            tmob.setcurrentroomid(self.getroomid())
            tmob.setcurrentzoneid(self.getzoneid())
            return True
        else:
            return False
    
    def removemob(self, tmob):
        try:
            self.mobs.remove(tmob)
            return True
        except:
            return False
    

    #####
    # SPAWNERS
    def addspawner(self, tspawner):
        if tspawner.getroomuid() == None:
            return False
        if tspawner.getobjuid() == None:
            return False
        
        tspawner.setticks( tspawner.getmaxticks() )
        self.spawners.append(tspawner)
        
    
    def newspawner(self, tobj, ticktime = 60):
        newspawner = worldobject.objectspawner(self, tobj, ticktime)
        
        if newspawner.getobjuid() != None:
            self.spawners.append(newspawner)
            newspawner.setticks( newspawner.getmaxticks() )        
    
    def getspawners(self):
        return self.spawners
    
    def dospawners(self):
        for s in self.spawners:
            
            if s.maxcountreached():
                continue
            
            s.dotick()
            
  
    

    def todict(self):
        
        tdict = worldobject.worldobject.todict(self)
        
        # room data
        tdict.update( {"data":self.data} )
        
        #####
        # NOTE : Remove item states, should be created with spawners
        """
        # inventory
        tdict.update( {"items":[] })
        for i in self.items:
            tdict["items"].append( i.todict() )
        
        # mobs
        tdict.update( {"mobs":[] } )
        for m in self.mobs:
            tdict["mobs"].append( m.todict() )
        """
        
        # spawners
        tdict.update( {"spawners":[] } )
        for s in self.spawners:
            tdict["spawners"].append( s.todict() )
        
        return tdict

    def fromJSON(self, jobj):
        
        # base class json load
        # not necessary since this is done in constructor
        #worldobject.worldobject.fromJSON(self, jobj)
        
        # room data
        self.data = jobj["data"]


        #####
        # NOTE : Remove item states, should be created with spawners        
        """
        # add items
        for i in jobj["items"]:
            newi = item.iteminstance(0, i)
            self.items.append(newi)
        
        # add mobs
        for m in jobj["mobs"]:
            newm = actor.mobinstance(0, m)
            self.mobs.append(newm)
        """
        
        # add spawners
        for s in jobj["spawners"]:
            news = worldobject.objectspawner(None, None, None)
            news.fromJSON(s)
            self.addspawner(news)
            

    def show(self):
        worldobject.worldobject.show(self)
        for d in self.data.keys():
            print "%s:%s" %(d, self.data[d])

        print "Spawners:"
        for s in self.spawners:
            print "  uid:%d - %s - @ %d/%d #%d" %(s.getobjuid(), s.getref().getnameex(), s.getticks(), s.getmaxticks(), s.getcount() )

        print "Items:"
        #for i in self.items:
        #    print "  iid:%d / refid(%d) : %s" %(i.getiid(), i.getuidref(), i.getrefname())
        self.items.show()
        
        print "Mobs:"
        for m in self.mobs:
            print "  iid:%d / refid(%d) : %s" %(m.getiid(), m.getuidref(), m.getnameex())

if __name__ == "__main__":
    import item
    
    item1 = item.item("rock")
    item2 = item.item("book")
    item1i = item1.create()
    item2i = item2.create()
    
    mob1 = actor.mob("dog")
    mob1i = mob1.create()
    
    
    room1 = room(0, 0, "Living Room")
    room1.setdescription("A pretty standard clean living room.  A large coffee table is covered in magazines.")
    room1.adddescriptor({"table":"The coffee table looks like it has been well used."})
    room1.adddescriptor({"magazine":"Some old National Geographics."})
    room1.newspawner(item2, 60)
    room1.additem(item1i)
    room1.additem(item2i)
    room1.addmob(mob1i)
    room1str = room1.toJSONstr()
    
    room1copy = room(1,1,"test", json.loads(room1str) )
    
    print "room1 json str:"
    print room1str
    
    print "\nroom1:"
    room1.show()
    
    print "\nroom1 copy:"
    room1copy.show()
    
    
