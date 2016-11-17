import item
import defs

# look at actor armor slots for reference
class Armor(item.Item):
	def __init__(self, name):
		item.Item.__init__(self, name)
		self.slotsUsed = []
		
	def setSlotUsed(self, sstr):
		
		# check if slot string is a valid armor slot
		if sstr in defs.armorSlots:
			self.slotsUsed.append(sstr)
			
			# remove duplicates
			self.slotsUsed = list( set(self.slotsUsed) )
		else:
			print "Armor set slots error, slot not valid:%s" %sstr
	
	def getSlotsUsed(self):
		return self.slotsUsed
	
	def isSlotUsed(self, sstr):
		
		return sstr in self.slotsUsed
	
	def show(self):
		item.Item.show(self)
		
		print "Slots used:"
		for slot in self.slotsUsed:
			print "    %s" %slot

