import item

class Weapon(item.Item):
	def __init__(self, name):
		item.Item.__init__(self, name)
		
