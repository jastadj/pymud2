import noun
import command

class Actor(object):
    def __init__(self, name = "unnamed"):
        self.noun = noun.Noun(name)
        self.noun.setProper(True)
        self.inventory = []
        
        self.attributes = {"max hp":10, "current hp":10}
        
        # weapon slots
        self.weaponSlots = {"right hand":None, "left hand":None}
        self.armorSlots = {"head":None, "neck":None, "torso":None, "left arm":None, "right arm":None}
        
    def getName(self):
        return self.noun.getName()
        
    def getExName(self):
        return self.noun.getExName()
    
    def getDescription(self):
        return self.noun.getDescription()

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
        if tattr in self.attributes.key():
            return self.attributes[tattr]
        else: return None
    
    def setName(self, name):
        self.noun.setName(name)
    
    def setDescription(self, desc):
        self.noun.setDescription(desc)
    
    def addItem(self, titem):
        try:
            self.inventory.append(titem)
        except:
            print "Error adding item to %s inventory!" %self.getName()  
    
    def addNewItem(self, idesc):
        newitem = command.getNewItem(idesc)
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
    
    def show(self):
        print "Name..........: %s" %self.getName()
        print "ExName........: %s" %self.getExName()
        print "ExName w/ Verb: %s" %self.noun.getExName(True)
        print "Desc..........: %s" %self.getDescription()
        print "Attributes:"
        for a in self.attributes.keys():
            print "%s = %d" %(a, self.attributes[a])
        print "Equipment:"
        for w in self.weaponSlots.keys():
            if self.weaponSlots[w] != None:
                print "%s:%s" %(w, self.weaponSlots[w].getExName())
        print "Items : %d" %len(self.getInventory())            

def saveActorToStrings(tactor):
    
    alines = []
    
    alines.append("actor_new:actor_new")
    
    alines += noun.saveNounToStrings(tactor.noun)
    
    
    # save attributes
    for a in tactor.attributes.keys():
        alines.append("actor_attribute:%s:%d" %(a, tactor.attributes[a]) )
    
    # save wielded items first
    for w in tactor.getWielded():    
        alines.append("actor_additem:%s" %w.getExName())
    # save carried items
    for i in tactor.inventory:
        alines.append("actor_additem:%s" %i.getExName() )
    
    # wielded items
    for w in tactor.weaponSlots.keys():
        if tactor.weaponSlots[w] != None:
            alines.append("actor_wield:%s:%s" %(w, tactor.weaponSlots[w].getExName() ) )
    
    return alines
    
def loadActorFromStrings(alines, tactor = None):
    
    newactor = None
    
    if tactor == None:
        newactor = Actor()
    else: newactor = tactor
    
    nounlines = []
    
    for line in alines:
        
        dfind = line.find(':')
        key = line[:dfind]
        val = line[dfind+1:]
        
        # noun
        if key.startswith("noun"):
            nounlines.append(line)
        # attributes
        elif key == "actor_attribute":
            afind = val.find(':')
            akey = val[:afind]
            aval = int( val[afind+1:] )
            
            newactor.attributes.update( {akey:aval})
        # items    
        elif key == "actor_additem":
            newitem = command.newItem(val)
           
            if newitem != None:
                newactor.inventory.append(newitem)
            else:
                print "Error adding item to actor, couldn't find item"

        # wielded
        elif key == "actor_wield":
            wfind = val.find(':')
            wslot = val[:wfind]
            witem = val[wfind+1:]
            
            # get inventory
            aitems = newactor.getInventory()
            founditems = command.findItemsInList(witem, aitems)
            newactor.wield(founditems[0])
            
    
    newactor.noun = noun.loadNounFromStrings(nounlines)
    
    if tactor == None:
        return newactor
if __name__ == "__main__":
    import defs
    import game
    import weapon
    import gameinit
    
    gameinit.gameInit()
    game.items =[]
    
    newweapon = weapon.Weapon("dagger")
    game.items.append(newweapon)
    
    print "New Actor:"
    newactor = Actor("billy")
    newactor.weaponSlots["right hand"] = newweapon
    astrings = saveActorToStrings(newactor)
    newactor.show()
    
    print "\nNew Actor copied from Actor 1 strings:"
    newactor2 = loadActorFromStrings(astrings)
    newactor2.show()