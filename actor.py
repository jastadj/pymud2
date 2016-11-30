import json
import worldobject
import hub
import item
import copy
import defs
import command

class actor(worldobject.worldobject):
    def __init__(self, name = "unnamed", jobj = None):
        
        # init base class data        
        worldobject.worldobject.__init__(self, name, jobj)
        
        # init class data
        self.data = {}
        self.attributes = {}
        
        # actor body parts
        self.bodyparts = {}
        self.bodyparts.update( {defs.BODYPART_HEAD:"head"} )
        self.bodyparts.update( {defs.BODYPART_NECK:"neck"} )
        self.bodyparts.update( {defs.BODYPART_TORSO:"torso"} )
        self.bodyparts.update( {defs.BODYPART_LEFTARM:"left arm"} )
        self.bodyparts.update( {defs.BODYPART_RIGHTARM:"right arm"} )
        self.bodyparts.update( {defs.BODYPART_LEFTHAND:"left hand"} )
        self.bodyparts.update( {defs.BODYPART_RIGHTHAND:"right hand"} )
        self.bodyparts.update( {defs.BODYPART_WAIST:"waist"} )
        self.bodyparts.update( {defs.BODYPART_LEFTLEG:"left leg"} )
        self.bodyparts.update( {defs.BODYPART_RIGHTLEG:"right leg"} )
        self.bodyparts.update( {defs.BODYPART_LEFTFOOT:"left foot"} )
        self.bodyparts.update( {defs.BODYPART_RIGHTFOOT:"right foot"} )

        
        
        # config attributes
        self.attributes.update( {"maxhp":1})
        
        #self.inventory = []
        
        # if json object supplied, load from that
        if jobj != None:
            self.fromJSON(jobj)
    
    def isactor(self):
        return True
    
    def isinstance(self):
        return issubclass(self.__class__, actorinstancedata)
    
    def getattribute(self, attribute):
        if attribute in self.attributes.keys():
            return self.attributes[attribute]
        else:
            return actorinstancedata.getattribute(self, attribute)
    
    def setattribute(self, attribute, val):
        if attribute in self.attributes.keys():
            self.attributes[attribute] = val
            return True
        else:
            return actorinstancedata.setattribute(self, attribute, val)
    
    def getbodyparts(self):
        return self.bodyparts
    
    def setbodyparts(self, bodyparts):
        self.bodyparts = bodyparts
    
    def todict(self):
        
        tdict = worldobject.worldobject.todict(self)
        
        tdict.update( {"data":self.data} )
        
        tdict.update( {"attributes":self.attributes} )
        
        tdict.update( {"bodyparts":self.bodyparts} )
        """
        tdict.update( {"inventory":[]} )
        for i in self.inventory:
            tdict["inventory"].append( i.todict() )
        """
        
        return tdict
    
    def fromJSON(self, jobj):
        
        self.data.update( jobj["data"] )
        
        self.attributes.update( jobj["attributes"] )
        
        self.bodyparts = jobj["bodyparts"]
        
        """
        for k in jobj["inventory"]:
            newi = item.iteminstance(0, k)
            self.inventory.append(newi)
        """
    def show(self):
        worldobject.worldobject.show(self)
        print "isinstance:%s" %self.isinstance()
        print "Attributes:"
        for a in self.attributes:
            print "  %s:%s" %(a, self.attributes[a])
        print "Body parts:"
        for b in self.bodyparts:
            print "  %s:%s" %(b, self.bodyparts[b])
        """
        print "Inventory:"
        for i in self.inventory:
            print "  iid:%d / refid(%d) : %s" %(i.getiid(), i.getuidref(), i.getrefname())
        """
   
class actorinstancedata(object):
    
    def __init__(self, tactor):
        
        self.pdata = {"currentzoneid":0, "currentroomid":0}
        self.pattributes = {"hp": tactor.getattribute("maxhp")}
        
        # inventory
        self.pinventory = item.pcontainer()
        
        # equipment layer
        self.pequipment = {"weapons":{}, "armor":{}, "clothing":{} }

        # combat
        self.combattarget = None
        self.combatticks = 0

        # regen
        self.healtick = 0
        self.healtickmax = 10
        self.healtickval = 1

    def isplayer(self):
        if self.__class__.__name__ == "character":
            return True
        else: return False

    def getnameex(self):
        if self.isplayer():
            return worldobject.worldobject.getnameex(self)
        else:
            return worldobject.worldobjectinstance.getref(self).getnameex()

    def getattribute(self, attribute):
        if attribute in self.pattributes.keys():
            return self.pattributes[attribute]
        else:
            if not self.isplayer():
                return self.getref().getattribute(attribute)
            
    
    def setattribute(self, attribute, val):
        if attribute in self.pattributes.keys():
            self.pattributes[attribute] = val
            return True
        else:
            if not self.isplayer():
                return self.getref().setattribute(attribute, val)

    def dotick(self):
        
        # if actor is dead
        if not self.isalive():
            self.dodeath()
            
        # check combat
        if self.incombat():
            command.docombat(self)
            
        # do heal tick (regen)
        if self.healtick <= 0:
            self.healtick = self.healtickmax
            self.modhealth(self.healtickval)
        else:
            self.healtick -= 1


        
    def incombat(self):
        if self.combattarget != None:
            if self.combattarget.getroom() == self.getroom():
                return True
        
        return False

    def getcombatspeed(self):
        return 5

    def isalive(self):
        if self.pattributes["hp"] <= 0:
            return False
        return True

    def dodeath(self):
        
        # remove self from current room mob list
        roomid = self.getcurrentroomid()
        zoneid = self.getcurrentzoneid()
        
        troom = hub.zones[zoneid].getroom(roomid)
        
        
        capname = self.getref().getnameex()[:1]
        capname = capname.upper()
        capname += self.getref().getnameex()[1:]
        deathmsg = "%s dies.\n" %capname
        command.doroombroadcast(troom, deathmsg)        
        
        if self.combattarget != None:
            self.combattarget.setcombattarget(None)
        self.combattarget = None
        
        
        # remove mob from room
        if not troom.removemob(self):
            print "ERROR REMOVING MOB FROM ROOM ON DEATH"
            print "ROOM MOBS:"
            for m in troom.getmobs():
                print " %s" %m.getref().getnameex()
        
        # add corpse to room
        tcorpse = hub.worldobjects[hub.finduidbyname("corpse")].create()
        tcorpse.initcustomnoun()
        tcorpse.getcustomnoun().setname("corpse of %s" %self.getnameex())
        troom.additem(tcorpse)
        
        # remove mob from instances
        hub.worldobjects_instance.pop(self.getiid(), None)




    def getroom(self):
        troom = hub.zones[ self.getcurrentzoneid()].getroom( self.getcurrentroomid() )
        return troom
        
    def getcurrentzoneid(self):
        return self.pdata["currentzoneid"]
    
    def getcurrentroomid(self):
        return self.pdata["currentroomid"]
        
    def setcurrentzoneid(self, zid):
        self.pdata["currentzoneid"] = zid
    
    def setcurrentroomid(self, rid):
        self.pdata["currentroomid"] = rid


    def getinventory(self):
        return self.pinventory.getitems()
        
    def getinventoryandequipment(self):
        ilist = self.getinventory()
        ilist += self.getequipped()
        return ilist
    
    def getequipped(self):
        elist = []
        for k in self.pequipment.keys():
            for e in self.pequipment[k].keys():
                elist.append( self.pequipment[k][e])
        return elist
    
    def additem(self, titem):
        if titem != None:
            return self.pinventory.additem(titem)
        else:
            return False
    
    def removeitem(self, titem):
        try:
            return self.pinventory.removeitem(titem)
        except:
            return False
    
    def modhealth(self, val):
        chealth = self.getattribute("hp")
        chealthmax = self.getattribute("maxhp")
        
        chealth += val
        if chealth > chealthmax:
            chealth = chealthmax
        
        self.setattribute("hp", chealth)
        
    def takehit(self, val):
        self.modhealth(-val)
    
    def getcombattarget(self):
        return self.combattarget
    
    def setcombattarget(self, tactorinstance):
        self.combattarget = tactorinstance
    
    def getattackroll(self):
        
        tdmg = 1
        
        twpn = self.getwielding()
            
        if twpn != None:
            tdmg = twpn.getref().weapon.getdamage()
        return tdmg
    
    def wield(self, titem):
        if not defs.BODYPART_RIGHTHAND in self.pequipment["weapons"]:
            self.pequipment["weapons"].update( {defs.BODYPART_RIGHTHAND:titem} )
            return self.pinventory.removeitem(titem)
        else: return False
        
    def unwield(self, titem):
        if defs.BODYPART_RIGHTHAND in self.pequipment["weapons"]:
            if self.pequipment["weapons"][defs.BODYPART_RIGHTHAND] == titem:
                self.pequipment["weapons"].pop(defs.BODYPART_RIGHTHAND, None)
                return self.pinventory.additem(titem)
        else: return False

    def getwielding(self):
        if defs.BODYPART_RIGHTHAND in self.pequipment["weapons"]:
            return self.pequipment["weapons"][defs.BODYPART_RIGHTHAND]
        return None
        
    def todict(self):
        tdict = {}
        
        # get persistent data
        tdict.update( {"pdata": self.pdata } )
        
        # get persistent attributes
        tdict.update( {"pattributes":self.pattributes } )

        # get persistent inventory
        tdict.update( {"pinventory":self.pinventory.todict()} )
        #for i in self.pinventory:
        #    tdict["pinventory"].append( i.todict() ) 
        
        # get equipment layers
        tdict.update( {"pequipment":{} } )
        for k in self.pequipment.keys():
            tdict["pequipment"].update( {k:{}} )
            
            for e in self.pequipment[k].keys():
                titem = self.pequipment[k][e]
                tdict["pequipment"][k].update( {int(e): titem.todict()} )
        
        return tdict

        
    def fromJSON(self, jobj):
        
        # get persistent dat
        self.pdata.update( jobj["pdata"] )
        
        # get persistent attributes
        self.pattributes.update( jobj["pattributes"] )
        
        # get persistent inventory
        #for k in jobj["pinventory"]:
        #    newi = item.iteminstance(0, k)
        #    self.pinventory.append(newi)
        self.pinventory = item.pcontainer()
        self.pinventory.fromJSON( jobj["pinventory"] )
            
        # get equipment layers
        self.pequipment = {}
        for k in jobj["pequipment"].keys():
            self.pequipment.update( {k:{}} )
            
            for e in jobj["pequipment"][k].keys():
                titem = item.iteminstance(0, jobj["pequipment"][k][e])
                self.pequipment[k].update( {int(e):titem} )
        
    def show(self):
        
        print "Persistent Data:"
        for p in self.pdata.keys():
            print "  %s:%s" %(p, self.pdata[p] )
        
        print "Persistent Attributes:"
        for p in self.pattributes.keys():
            print "  %s:%s" %(p, self.pattributes[p])
        
        print "Inventory:"
        self.pinventory.show()
        #for i in self.pinventory:
        #    print "  iid:%d / refid(%d) : %s" %(i.getiid(), i.getuidref(), i.getrefname())
            
        print "Equipment:"
        for k in self.pequipment.keys():
            print "  %s" %k
            for e in self.pequipment[k].keys():
                print "    %s:%s" %(e, self.pequipment[k][e].getref().getnameex() )

class mob(actor):
    def __init__(self, name = "unnamed", jobj = None):

        self.mobdata = {}
        
        # init base class data
        actor.__init__(self, name, jobj)
        
        # init class data
        # note: data already is derived from actor, only update dict
        
        if jobj != None:
            self.fromJSON(jobj)
        
    def todict(self):
        
        # get actor data
        tdict = actor.todict(self)
        
        # get mob data
        tdict.update( {"mobdata":{} } )
        
        return tdict
    
    def fromJSON(self, jobj):
        
        # get actor data
        actor.fromJSON(self, jobj)
        
        # get mob data
        self.mobdata.update( jobj["mobdata"] )
        
    def show(self):
        # show from base class
        actor.show(self)
    
    def create(self):
        newi = mobinstance(self.uid)
        return newi

class mobinstance(worldobject.worldobjectinstance, actorinstancedata):
    
    def __init__(self, uidref, jobj = None):
        
        # init base class data
        worldobject.worldobjectinstance.__init__(self, uidref, jobj)
        actorinstancedata.__init__(self, self.getref())

    def dotick(self):
        actorinstancedata.dotick(self)

    def todict(self):
        tdict = worldobject.worldobjectinstance.todict(self)
        
        tdict.update( actorinstancedata.todict(self) )
        
        return tdict
        
    def fromJSON(self, jobj):
        
        worldobject.worldobjectinstance.fromJSON(self, jobj)
        
        actorinstancedata.fromJSON(self, jobj)
    
    def show(self):
        worldobject.worldobjectinstance.show(self)
        actor.show(self.getref())
        actorinstancedata.show(self)

     
if __name__ == "__main__":
    
    print "\nMob 1:"
    mob1 = mob("dog")
    mob1.setattribute("maxhp", 5)
    mob1.show()
    
    print "\nMob 1 Instance:"
    mob1i = mob1.create()
    mob1i.show()
