import defs
import game
from tools import *

ITEMTYPES = ["Item", "Weapon", "Armor"]

class Item(object):
    def __init__(self, name):
        self.sproperties = {"name":name, "desc":"no description"}
        self.bproperties = {}
        self.iproperties = {}
        self.adjectives = []
        # try to determine article
        vowels = ['a','e','i','o','u']
        if name[0] in vowels:
            self.sproperties.update({"article":"an"} )
        else:
            self.sproperties.update({"article":"a"} )
        
        # set grammar
        self.bproperties.update( {"proper":False} )

    def descMatches(self, dstr):
        
        dstr = dstr.split()
        dlen = len(dstr)
        
        if dlen == 1:
            if dstr[0] == self.getName():
                return True
        else:
            for d in dstr:
                if d == dstr[-1]:
                    if d != self.getName():
                        return False
                elif d not in self.adjectives:
                    return False
    def getType(self):
        return self.__class__.__name__
    
    def getDesc(self):
        #debug
        self.show()
        return self.sproperties["desc"]

    def addAdjective(self, astr):
        self.adjectives.append(astr)
    
    def getDescName(self):
        dstr = ""
        
        if len(self.adjectives) != 0:
            dstr = " ".join(self.adjectives) + " " + self.getName()
        else: 
            dstr = self.getName()
            
        return dstr
    
    def getName(self):
        return self.sproperties["name"]
    
    def getArticle(self):
        return self.sproperties["article"]
    
    def show(self):
        print "Item Type:%s" %self.getType()
        print "Desc Name:%s" %self.getDescName()
        
        for s in self.sproperties.keys():
            print "%s=%s" %(s, self.sproperties[s])
        
        for a in self.adjectives:
            print "adjective:%s" %a
        
        for i in self.iproperties.keys():
            print "%s=%d" %(i, self.iproperties[i])

def loadItemFromStrings(istrings):
    
    if istrings == None:
        print "Error loading item from strings, strings null!"
        return None
    
    if len(istrings) == 0:
        return None
    
    itemtype = None
    
    # determine item type
    for line in istrings:
        if line.startswith("type:"):
            tfind = line.find(':')
            itemtype = line[tfind+1:]
    
    # check that item type is valid
    if not itemtype in ITEMTYPES:
        itemtype = None
        
    if itemtype == None:
        print "Error loading item, type unknown!"
        return None
    
    newitem = None
    if itemtype == "Item": newitem = Item("unnamed")
    elif itemtype == "Weapon": newitem = game.WEAPON("unnamed")
    elif itemtype == "Armor": newitem = game.ARMOR("unnamed")
    
    for line in istrings:
        if line != "":
            delim = line.find(':')
            key = line[:delim]
            val = line[delim+1:]
            
            # string properties
            if key in newitem.sproperties:
                newitem.sproperties[key] = val
            
            # adjectives
            elif key == "adjective":
                newitem.addAdjective(val)
            
            # boolean properties
            elif key in newitem.bproperties:
                if val == "True": val = True
                elif val == "False":val = False
                newitem.bproperties[key] = val
                
            elif key in newitem.iproperties:
                newitem.iproperties[key] = int(val)
                
    return newitem

def saveItemToStrings(titem):
    
    istring = []
    
    istring.append("\nITEM:\n")

    # write item type
    istring.append("type:%s\n" %titem.getType())
    

    # write string properties
    for s in titem.sproperties.keys():
        istring.append("%s:%s\n" %(s, titem.sproperties[s]) )
    
    # write adjectives
    for a in titem.adjectives:
        istring.append("adjective:%s\n" %a)
    
    # write boolean properties
    for b in titem.bproperties.keys():
        istring.append("%s:%s\n" %(b, titem.bproperties[b]) )
    
    # write integer properties
    for i in titem.iproperties.keys():
        istrong.append("%s:%d\n" %(i, titem.iproperties[i] ) )
    
    return istring

def loadItems():
    
    fp = defs.ITEMS_FILE
    
    game.items = []
    game.items_common = []
    
    # if items file exists
    if createNewFile(fp) == None:
        
        ilines = []
        
        with open(fp, "r") as rf:
            for line in rf:
                line = line[:-1]
                
                # if line is not blank, process
                if line != "":
                    delim = line.find(':')
                    key = line[:delim]
                    val = line[delim+1:]
                    
                    # if line is item identifier, create new item
                    # off load read in lines for loading, then reset
                    if line == "ITEM:":
                        if ilines != []:
                            game.items_common.append(loadItemFromStrings(ilines) )
                        
                        ilines = []
                    
                    # add item line parameter
                    else:
                        ilines.append(line)
        
        #offload last entry
        if len(ilines) != 0:
            game.items_common.append(loadItemFromStrings(ilines))
            ilines = []
        
        rf.close()
    
    # else new items file created
    else:
        
        print "No item file found.  Creating defaults..."
        # create default item
        newitem = Item("rock")
        
        game.items_common.append(newitem)
    
    # concatenate common items to master items list
    game.items += game.items_common 
        
def saveItems():
    
    fp = defs.ITEMS_FILE
    
    createNewFile(fp)
    
    wf = open(fp, "w")
    
    for i in game.items_common:
        istrings = saveItemToStrings(i)
        
        for line in istrings:
            wf.write(line)

if __name__ == "__main__":
    
    import weapon
    import game
    import armor
    
    game.WEAPON = weapon.Weapon
    game.ARMOR = armor.Armor
    game.ITEM = Item
    
    defs.configTestMode()
    
    print ""
    
    game.items_common = []
    game.items = []
    
    def showItems():
        for i in game.items:
            print ""
            i.show()
    
    
    newitem = game.ITEM("rock")
    game.items_common.append(newitem)
    newitem = game.WEAPON("sword")
    newitem.addAdjective("long")
    game.items_common.append(newitem)
    newitem = game.ARMOR("cap")
    newitem.addAdjective("leather")
    game.items_common.append(newitem)
    
    game.items += game.items_common
    
    print "Saving items..."
    saveItems()
    showItems()

    print "Loading items..."
    game.items = []
    game.items_common = []
    loadItems()
    showItems()

