import noun
import game

class WorldObject(noun.Noun):
    def __init__(self, name = "unnamed"):
        noun.Noun.__init__(self, name)
        
    
    def getType(self):
        return self.__class__.__name__
    
    """
    def saveToStrings(self):
		return noun.Noun.saveToStrings(self)
    
    def loadFromStrings(self, tstrings):
		noun.Noun.loadFromStrings(self, tstrings)
    """
    
    def doTick(self):
        
        self.onTick()
        
        for c in self.getChildren():
            c.doTick()
    
    def onTick(self):
        pass
    
    def getChildren(self):
        return []
    
    def show(self):
        print "Type:%s" %self.getType()
        print "Name:%s" %self.getName()
        print "ExName:%s" %self.getExName()
        print "Description:\n%s" %self.getDescription()
        
if __name__ == "__main__":

    testobj = WorldObject("basketball")
    testobj.addAdjective("worn")
    testobj.show()
    
    tstrings = testobj.saveToStrings()
    
    for line in tstrings:
        print line
    
    
    print "\n\n"
    testobj2 = WorldObject()
    testobj2.loadFromStrings(tstrings)
    testobj2.show()
