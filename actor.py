import command

class Actor(object):
	def __init__(self):
		self.sproperties = {"name":"unnamed", "desc":"nodesc"}
		self.iproperties = {}
		self.inventory = []

	def getName(self):
		return self.sproperties["name"]
	
	def getDesc(self):
		return self.sproperties["desc"]

	def hasItem(self, titem):		
		return titem in self.inventory
		
	def getInventory(self):
		return self.inventory
	
	def setName(self, name):
		self.sproperties["name"] = name
	
	def setDesc(self, desc):
		self.sproperties["desc"] = desc
	
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