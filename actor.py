import noun
import command

class Actor(object):
    def __init__(self, name = "unnamed"):
        self.noun = noun.Noun(name)
        self.noun.setProper(True)
        self.desc = "no desc"
        self.inventory = []

    def getName(self):
        return self.noun.getName()
        
    def getExName(self):
        return self.noun.getExName()
    
    def getDesc(self):
        return self.desc

    def hasItem(self, titem):       
        return titem in self.inventory
        
    def getInventory(self):
        return self.inventory
    
    def setName(self, name):
        self.noun.setName(name)
    
    def setDesc(self, desc):
        self.desc = desc
    
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

def saveActorToStrings(tactor):
    
    alines = []
    
    alines.append("actor_new:actor_new")
    
    alines += noun.saveNounToStrings(tactor.noun)
    
    alines.append("actor_desc:%s" %tactor.desc)
    
    for i in tactor.inventory:
        alines.append("actor_additem:%s" %i.getExName() )
        
    return alines
    
def loadActorFromStrings(alines, tactor = None):
    
    if tactor == None:
        newactor = Actor()
    
    else: newactor = tactor
    
    nounlines = []
    
    for line in alines:
        
        dfind = line.find(':')
        key = line[:dfind]
        val = line[dfind+1:]
        
        if key.startswith("noun"):
            nounlines.ppend(line)
        elif key == "actor_desc":
            newactor.desc = val
        elif key == "actor_additem":
            newitem = command.newItem(val)
           
            if newitem != None:
                newactor.inventory.append(newitem)
            else:
                print "Error adding item to actor, couldn't find item"
    
    if tactor == None:
        return newactor