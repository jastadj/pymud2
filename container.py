import item
import command

class Container(item.Item):
    def __init__(self,name = "unnamed"):
        item.Item.__init__(self, name)
        self.inventory = []
    
    def hasItem(self, titem):
        
        if titem in self.inventory:
            return True
        else:
            return False
    
    def addItem(self, titem):
        
        if titem == None:
            print "Error adding item to container, item isnull!"
            return
        
        self.inventory.append(titem)
    
    def removeItem(self, titem):
        
        if titem == None:
            print "Error removing item from container, item null!"
            return
        
        # check that item is in container
        if self.hasItem(titem):
            self.inventory.remove(titem)
    
    def addNewItem(self, istr):
        newitem = command.newItem(istr)
        
        if newitem == None:
            print "Error adding new item to container, item null!"
            return
        
        self.addItem(newitem)
    
    def getItems(self):
        return self.inventory
        
