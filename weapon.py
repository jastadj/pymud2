import item

class Weapon(item.Item):
    def __init__(self, name):
        item.Item.__init__(self, name)
        self.damage = 1
        self.hands = 1
        
    def getDamage(self):
        return self.damage
    
    def setDamage(self, dmg):
        self.damage = dmg
    
    def getHands(self):
        return self.hands
        
    def setHands(self, hands):
        self.hands = hands
    
    def show(self):
        item.Item.show(self)
        print "Damage       :%d" %self.getDamage()
        print "Hands        :%d" %self.getHands()