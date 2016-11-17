import defs
import game
import noun
from tools import *

ITEMTYPES = ["Item", "Weapon", "Armor"]

class Item(object):
    def __init__(self, name):
        self.noun = noun.Noun(name)
        self.noun.setProper(False)
        
    def getType(self):
        return self.__class__.__name__
    
    def test(self):
        print "this is a test"
    
    def getName(self):
        return self.noun.getName()
    
    def getExName(self):
        return self.noun.getExName()
    
    def getArticle(self):
        return self.noun.getArticle()
    
    def getDescription(self):
        return self.noun.getDescription()
        
    def setDescription(self, desc):
        self.noun.setDescription(desc)
    
    def isWeapon(self):
        return issubclass( type(self), game.WEAPON)
    
    def isArmor(self):
        return issubclass( type(self), game.ARMOR)
    
    def show(self):
        print "Item Type    :%s" %self.getType()
        print "isWeapon     :%s" %self.isWeapon()
        print "isArmor      :%s" %self.isArmor()
        print "Name         :%s" %self.getName()
        print "Extended Name:%s" %self.getExName()
        print "Description  :%s" %self.getDescription()

def loadItemFromStrings(istrings):
    
    nounstrings = []
    
    newitem = None
    itemtype = None
    
    # determine item type    
    for line in istrings:
        
        dfind = line.find(':')
        
        key = line[:dfind]
        val = line[dfind+1:]
        
        if line.startswith("noun"): nounstrings.append(line)
        elif key == "item_new":
            if val == "Item": newitem = Item("unnamed")
            elif val == "Weapon": newitem = game.WEAPON("unnamed")
            elif val == "Armor": newitem = game.ARMOR("unnamed")
            
            itemtype = newitem.getType()
        
        # weapon data
        if newitem.isWeapon() == "Weapon":
            if key == "weapon_damage":
                newitem.setDamage(int(val))
            elif key == "weapon_hands":
                newitem.setHands(int(val))
                
        # armor data
        if newitem.isArmor() == "Armor":
            if key == "armor_slot":
                newitem.setSlotUsed(val)

    # load and set noun from strings
    newitem.noun = noun.loadNounFromStrings(nounstrings)
    
    return newitem
        

def saveItemToStrings(titem):
    
    istrings = []
    
    itemtype = titem.getType()
    
    istrings.append("item_new:%s" %itemtype)
    istrings += noun.saveNounToStrings(titem.noun)
    
    if titem.isWeapon():
        istrings.append("weapon_damage:%d" %titem.getDamage())
        istrings.append("weapon_hands:%d" %titem.getHands())
    
    if titem.isArmor():
        for s in titem.getSlotsUsed():
			istrings.append("armor_slot:%s" %s)
    
    return istrings
    


def loadItems():
    
    fp = defs.ITEMS_FILE
    
    game.items_common = []
    
    def processILines(t_ilines):
        # if there are item lines that need to be processed
        if len(t_ilines) != 0:
            
            newitem = loadItemFromStrings(t_ilines)
            
            if newitem != None:
                game.items_common.append(newitem)
            else:
                print "Error loading common item from strings!"
    
    # if items file exists
    if createNewFile(fp) == None:
    
        ilines = []
        
        with open(fp, "r") as f:
            for line in f:
                
                # trim newline
                line = line[:-1]
                
                # if line is blank
                if line == "": continue
                
                # if new item found
                if line.startswith("item_new"):
                    
                    processILines(ilines)
                    ilines = []
                
                # else, just pump in lines read for item lines
                ilines.append(line)
            
            # process last element if necessary
            processILines(ilines) 
            ilines = []
        
        f.close()
        
    # items file does not exist
    else:
        pass
    
    # transfer loaded common items to main game items
    game.items += game.items_common
    
        
def saveItems():
    
    fp = defs.ITEMS_FILE
    
    createNewFile(fp)
    
    f = open(fp, "w")
    
    for i in game.items_common:
        ilines = saveItemToStrings(i)
        
        for line in ilines:
            f.write("%s\n" %line)
        
        f.write("\n")
    
    f.close()
    
if __name__ == "__main__":
    
    # configure test environment
    import gameinit
    gameinit.gameInitTest()
    
    # if there are no items loaded, do this test
    if len(game.items_common) == 0:
    
        newitem = Item("rock")
        
        print "Test Item:"
        newitem.show()
        
        print "\nTest Item to Strings:"
        istrings = saveItemToStrings(newitem)
        for i in istrings:
            print i
            
        #######
        print "\n\nLoading item 2 from item 1 strings..."
        newitem2 = loadItemFromStrings(istrings)
        newitem2.show()
        
        game.items_common.append(newitem)
    
        #####
        newitemweapon = game.WEAPON("sword")
        newitemweapon.noun.addAdjective("long")
        newitemweapon.setDescription("A pretty sharp looking sword.")
        newitemweapon.setDamage(3)
        game.items_common.append(newitemweapon)
        
        #####
        newitemweapon2 = game.WEAPON("axe")
        newitemweapon2.noun.addAdjective("battle")
        newitemweapon2.setDescription("A grisly looking battle axe")
        newitemweapon2.setDamage(5)
        newitemweapon2.setHands(2)
        game.items_common.append(newitemweapon2)
        
        #####
        newitemarmor = game.ARMOR("cap")
        newitemarmor.noun.addAdjective("leather")
        newitemarmor.setDescription("A cap made out of boiled leather.")
        newitemarmor.setSlotUsed("head")
        game.items_common.append(newitemarmor)
    
        print "Saving items to file..."
        saveItems()
    
    # else, items loaded, print them
    else:
        print "\n\nItems loaded from file"
        for i in game.items:
            print "\n"
            i.show()
