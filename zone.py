import json
import defs
import hub
import room
from tools import *

class zone(object):
    
    def __init__(self, zoneid, zonefile, ignorefile = False):
        
        # zone data
        self.data = {"zid":zoneid, "ridcount":0, "filename":zonefile}
        self.data.update( {"name":"unnamed", "description":"no descripiton"} )
        
        # dicts
        self.rooms = {}
        
        # get filename and path of target zone file
        fp = defs.ZONES_PATH + zonefile
        
        if ignorefile:
            createNewFile(fp)
        # if zone file exists
        elif createNewFile(fp) == None:
            f = open(fp, "r")
            
            jstrings = f.read()
            
            self.fromJSON( json.loads(jstrings) )
                    
            f.close()

    def count(self):
        return len(self.rooms.keys())
            
    def getid(self):
        return self.data["zid"]

    def getfilename(self):
        return self.data["filename"]

    def getname(self):
        return self.data["name"]
        
    def getdescription(self):
        return self.data["description"]
    
    def getroom(self, rid):
        if rid in self.rooms:
            return self.rooms[rid]
        
        else: return None
        
    def newroom(self, name = "unnamed"):
        
        # acquire new room id
        newroomid = self.data["ridcount"]
        self.data["ridcount"] += 1
        
        # create new room
        newroom = room.room(self.getid(), newroomid, name)
        
        # update zone room dict
        self.rooms.update( {newroomid:newroom} )

    def connectrooms(self, r1, r1exit, r2, r2exit):
        
        r1num = None
        r2num = None
        
        if type(r1) == int:
            r1 = self.getroom(r1)
        if type(r2) == int:
            r2 = self.getroom(r2)
        
        r1num = r1.getroomid()
        r2num = r2.getroomid()
        
        if r1 == None or r2 == None: return False
        
        r1.addexit(r1exit, r2num)
        r2.addexit(r2exit, r1num)
        
        return True
    
    def todict(self):
        tdict = {}
        
        tdict.update( {"data":self.data } )
        
        tdict.update ( {"rooms":{} } )
        for r in self.rooms.keys():
            troom = self.rooms[r]
            tdict["rooms"].update( {troom.getroomid():troom.todict() } )
        
        return tdict
    
    def toJSONstr(self):
        return json.dumps( self.todict() )

    def fromJSON(self, jobj):
        
        self.data = jobj["data"]
        
        for r in jobj["rooms"].keys():
            
            newroom = room.room( 0, 0, "unnamed", jobj["rooms"][r] )
            
            self.rooms.update( { newroom.getroomid(): newroom} )
            

    def save(self):
        
        # get filename and path of target zone file
        fp = defs.ZONES_PATH + self.data["filename"]
        
        f = open(fp, "w")

        # write zone data
        f.write( self.toJSONstr())

        f.close()
    
    def show(self):   
             
        print "Zone Data:"
        print "----------"
        for d in self.data.keys():
            print "  %s = %s" %(d, self.data[d])
        
        print "Zone Rooms:"
        print "  room count = %d" %self.count()
        for r in self.rooms.keys():
            print "  %d - %s" %( r, self.rooms[r].getname() )
            
        
if __name__ == "__main__":

    defs.configtestmode()
    
    if not fileExists( defs.ZONES_PATH + "test.zn"):
        newzone = zone(0, "test.zn")
        newzone.newroom("Bathroom")
        troom = newzone.getroom(0)
        troom.setdescription("A gross bathroom.")
        newzone.save()
    
    else:
        newzone = zone(0, "test.zn")
    
    print "\n"
    newzone.show()

    print "\n"
    hub.showworldobjects()
