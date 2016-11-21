import defs
import worldobject
import command

class Actor(worldobject.WorldObject):
    def __init__(self, name = "unnamed"):
        worldobject.WorldObject.__init__(self, name)
        self.inventory = []
        
        self.attributes = {"max hp":10, "current hp":10}
        
        self.combatTarget = None
        
        # init weapon slots
        self.weaponSlots = {}
        for wslot in defs.weaponSlots:
            self.weaponSlots.update( {wslot:None} )
        
        # init armor slots
        self.armorSlots = {}
        for aslot in defs.armorSlots:
            self.armorSlots.update( {aslot:None} )

    def isPlayer(self):
        if self.getType() == "Character":
            return True
        else: return False

    def hasItem(self, titem):       
        return titem in self.inventory
        
    def getInventory(self):
        return self.inventory
    
    def getWielded(self):
        
        eitems = []
        
        for e in self.weaponSlots.keys():
            if self.weaponSlots[e] != None:
                eitems.append(self.weaponSlots[e])
        
        return eitems
    
    def getWorn(self):
        
        eitems = []
        
        for e in self.armorSlots.keys():
            if self.armorSlots[e] != None:
                eitems.append(self.armorSlots[e])
    
        return eitems    
    
    def getEquipment(self):
        eitems = []
        
        eitems += self.getWielded()
        eitems += self.getWorn()
    
        return eitems
    
    def getAttribute(self, tattr):
        if tattr in self.attributes.keys():
            return self.attributes[tattr]
        else: return None
    
    def addItem(self, titem):
        try:
            self.inventory.append(titem)
        except:
            print "Error adding item to %s inventory!" %self.getName()  
    
    def addNewItem(self, idesc):
        newitem = command.newItem(idesc)
        if newitem != None:
            self.addItem(newitem)
        else:
            print "Error adding new item to character, item not found"

    def removeItem(self, titem):
        
        if not self.hasItem(titem):
            print "Error removing %s from %s, not in inventory!" %(titem.getName(),self.getName())
            return False
        try:
            self.inventory.remove(titem)
            return True
        except:
            print "Error removing item from %s inventory!" %self.getname()
            return False
    
    def wield(self, tweapon):
        
        # if item is not in inventory
        if tweapon not in self.inventory: return "You are not carrying that!"
        
        # if item is not a weapon
        if not tweapon.isWeapon(): return "That is not a weapon!"
        
        # hands required for wielding
        handsreq = tweapon.getHands()
        
        # find free hands
        freehands = 0
        for c in self.weaponSlots.keys():
            if self.weaponSlots[c] == None:
                freehands += 1
        
        # not enough free hands to use weapon
        if freehands < handsreq: return "Not enough free hands to wield this weapon!"
        
        # assign weapon to available slot(s)
        for c in self.weaponSlots.keys():
            if handsreq <= 0: break
            if self.weaponSlots[c] == None:
                self.weaponSlots[c] = tweapon
                handsreq -= 1
        
        # remove item from inventory
        self.removeItem(tweapon)
        
        return True
    
    def setAttribute(self, tattr, val):
        if tattr in self.attributes:
            self.attributes[tattr] = val
            return True
        else: return False
            
    def getCombatTarget(self):
        return self.combatTarget
    
    def setCombatTarget(self, tactor):
        self.combatTarget = tactor
    
    def inCombat(self):
        if self.combatTarget != None: return True
        else: return False

    def isAlive(self):
        if self.getAttribute("current hp") > 0:
            return True
        else: return False

    def onTick(self):
        
        if not self.isAlive():
            self.doDeath()
        
        elif self.inCombat():
            command.doAttack(self)    
    
    def show(self):
        worldobject.WorldObject.show(self)
        print "Attributes:"
        for a in self.attributes.keys():
            print "    %s = %d" %(a, self.attributes[a])
        print "Equipped:"
        for w in self.weaponSlots.keys():
            if self.weaponSlots[w] != None:
                print "    %s:%s" %(w, self.weaponSlots[w].getExName())
        print "Items:"
        for i in self.getInventory():
            print "    %s" %i.getExName()

    def saveToStrings(self):
        
        tstrings = []
        
        # save actor entry type
        tstrings.append("actor:%s" %self.getType() )
        
        # save base class data
        tstrings += worldobject.WorldObject.saveToStrings(self)
        
        
        # save attributes
        for a in self.attributes.keys():
            tstrings.append("%s_attribute:%s:%d" %(self.getType(), a, self.attributes[a]) )
        
        # save wielded items first
        for w in self.getWielded():    
            tstrings.append("%s_additem:%s" %( self.getType() ,w.getExName()) )
        
        # save carried items
        for i in self.inventory:
            tstrings.append("%s_additem:%s" %( self.getType(), i.getExName() ) )
            
        
        # wield items
        for w in self.weaponSlots.keys():
            if self.weaponSlots[w] != None:
                tstrings.append("%s_wield:%s:%s" %( self.getType() , w, self.weaponSlots[w].getExName() ) )
        
        return tstrings
    
    def loadFromStrings(self, tstrings):
        
        # load base class data from strings
        worldobject.WorldObject.loadFromStrings(self, tstrings)
        
        for line in tstrings:
            
            dfind = line.find(':')
            key = line[:dfind]
            val = line[dfind+1:]
            
            # attributes
            if key == "%s_attribute" %self.getType():
                afind = val.find(':')
                akey = val[:afind]
                aval = int( val[afind+1:] )
                
                self.attributes.update( {akey:aval})
                
            # items    
            elif key == "%s_additem" %self.getType():
                newitem = command.newItem(val)
               
                if newitem != None:
                    self.inventory.append(newitem)
                else:
                    print "Error adding item to actor, couldn't find item"

            # wielded
            elif key == "%s_wield" %self.getType():
                wfind = val.find(':')
                wslot = val[:wfind]
                witem = val[wfind+1:]
                
                # get inventory
                aitems = self.getInventory()
                founditems = command.findItemsInList(witem, aitems)
                self.wield(founditems[0])
    
    def getChildren(self):
        
        children = []
        children += self.inventory
        children += self.getEquipment()
        
        return children
        
        
if __name__ == "__main__":
    import gameinit
    gameinit.gameInitTest()
    
    # create new actor
    newactor = Actor("orc")
    newactor.addNewItem("sword")
    newactor.show()

    # get new actor's strings
    astrings = newactor.saveToStrings()

    # print strings
    for line in astrings:
        print line

    # copy actor
    bactor = Actor()
    bactor.loadFromStrings(astrings)
    bactor.setName("orc general")
    bactor.show()
    
