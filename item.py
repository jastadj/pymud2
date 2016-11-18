import defs
import worldobject
import game
from tools import *

class Item(worldobject.WorldObject):
    def __init__(self, name = "unnamed"):
        worldobject.WorldObject.__init__(self, name)
    
    def isWeapon(self):
        return issubclass( type(self), game.OBJECT_CLASSES["Weapon"])
    
    def isArmor(self):
        return issubclass( type(self), game.OBJECT_CLASSES["Armor"])
    
    def show(self):
        worldobject.WorldObject.show(self)
        print "isWeapon:%s" %self.isWeapon()
        print "isArmor:%s" %self.isArmor()
        
        if self.isWeapon():
            print "Weapon Data:"
            print "    Damage:%d" %self.getDamage()
            print "    Hands :%d" %self.getHands()
        
        if self.isArmor():
            print "Armor Data:"
            print "    Slots used:"
            for slot in self.slotsUsed:
                print "        %s" %slot            

    def saveToStrings(self):
        
        istrings = []
        
        # save item
        istrings.append("item:%s" %self.getType() )
        
        # save base class data (noun)
        istrings += worldobject.WorldObject.saveToStrings(self)
        
        if self.isWeapon():
            istrings.append("%s_weapon_damage:%d" %(self.getType(), self.getDamage()) )
            istrings.append("%s_weapon_hands:%d" %(self.getType(), self.getHands()) )
        
        if self.isArmor():
            for s in self.getSlotsUsed():
                istrings.append("%s_armor_slot:%s" %( self.getType(),s) )
        
        return istrings


    def loadFromStrings(self, tstrings):
        
        # load baseclass
        worldobject.WorldObject.loadFromStrings(self, tstrings)
        
        # load item data from strings
        for line in tstrings:
            
            dfind = line.find(':')
            key = line[:dfind]
            val = line[dfind+1:]
            
            # weapon data
            if self.isWeapon():
                if key == "%s_weapon_damage" %self.getType():
                    self.setDamage(int(val))
                elif key == "%s_weapon_hands" %self.getType():
                    self.setHands(int(val))
                    
            # armor data
            if self.isArmor():
                if key == "%s_armor_slot" %self.getType():
                    self.setSlotUsed(val)

    
if __name__ == "__main__":
    
    # configure test environment
    import gameinit
    gameinit.gameInitTest()
    
    # if there are no items loaded, do this test
    if len(game.items_common) == 0:
    
        newitem = game.OBJECT_CLASSES["Item"]("rock")
        
        print "Test Item:"
        newitem.show()
        
        print "\nTest Item to Strings:"
        istrings = newitem.saveToStrings()
        for i in istrings:
            print i
            
        #######
        print "\n\nLoading item 2 from item 1 strings..."
        newitem2 = game.OBJECT_CLASSES[newitem.getType()]()
        newitem2.loadFromStrings(istrings)
        newitem2.show()
        game.items_common.append(newitem)
    
        #####
        newitemweapon = game.OBJECT_CLASSES["Weapon"]("sword")
        newitemweapon.addAdjective("long")
        newitemweapon.setDescription("A pretty sharp looking sword.")
        newitemweapon.setDamage(3)
        game.items_common.append(newitemweapon)
        
        #####
        newitemweapon2 = game.OBJECT_CLASSES["Weapon"]("axe")
        newitemweapon2.addAdjective("battle")
        newitemweapon2.setDescription("A grisly looking battle axe")
        newitemweapon2.setDamage(5)
        newitemweapon2.setHands(2)
        game.items_common.append(newitemweapon2)
        
        #####
        newitemarmor = game.OBJECT_CLASSES["Armor"]("cap")
        newitemarmor.addAdjective("leather")
        newitemarmor.setDescription("A cap made out of boiled leather.")
        newitemarmor.setSlotUsed("head")
        game.items_common.append(newitemarmor)
    
        print "Saving items to file..."
        gameinit.saveItems()
    
    # else, items loaded, print them
    else:
        print "\n\nItems loaded from file"
        for i in game.items:
            print "\n"
            i.show()
