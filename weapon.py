import item

class Weapon(item.Item):
    def __init__(self, name = "unnamed"):
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
