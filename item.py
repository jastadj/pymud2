import defs
import game
from tools import *

class Item(object):
	def __init__(self, name):
		self.properties = {"name":name, "desc":"no description"}
		self.adjectives = []
		# try to determine article
		vowels = ['a','e','i','o','u']
		if name[0] in vowels:
			self.properties.update({"article":"an"} )
		else:
			self.properties.update({"article":"a"} )
		
		# set grammar
		self.properties.update( {"proper":False} )

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
				
	def getDesc(self):
		return self.properties["desc"]

	def addAdjective(self, astr):
		self.adjectives.append(astr)
	
	def getDescName(self):
		dstr = " ".join(self.adjectives) + " " + self.getName()
		return dstr
	
	def getName(self):
		return self.properties["name"]
	
	def getArticle(self):
		return self.properties["article"]
	
	def show(self):
		print "Desc Name:%s" %self.getDescName()
		
		for i in self.properties.keys():
			print "%s=%s" %(i, self.properties[i])
		for a in self.adjectives:
			print "adjective:%s" %a

def loadItemFromStrings(istrings):
	
	if istrings == None:
		print "Error loading item from strings, strings null!"
		return None
	
	if len(istrings) == 0:
		return None
	
	newitem = Item("unnamed")
	
	for line in istrings:
		if line != "":
			delim = line.find(':')
			key = line[:delim]
			val = line[delim+1:]
			
			# if key is a properties key, set it
			if key in newitem.properties:
				#print "setting %s to %s" %(key, val)
				if key == "proper":
					if val == "True": val = True
					elif val == "False": val = False
				else:
					newitem.properties[key] = val
			if key == "adjective":
				newitem.addAdjective(val)
	return newitem

def saveItemToStrings(titem):
	
	istring = []
	
	istring.append("ITEM:\n")
		
	for p in titem.properties.keys():
		istring.append("%s:%s\n" %(p, titem.properties[p]) )
	
	for a in titem.adjectives:
		istring.append("adjective:%s\n" %a)
	
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
					
					# if key is a properties key, set it
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
	
	defs.configTestMode()
	
	print ""
	
	game.items_common = []
	game.items = []
	
	def showItems():
		for i in game.items:
			print ""
			i.show()
	
	
	newitem = Item("sword")
	game.items_common.append(newitem)
	newitem.addAdjective("long")
	newitem = Item("cap")
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

