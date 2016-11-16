
DIRECTIONS = ["north","south","east","west", "up","down"]

ZONES_PATH = "./zones/"
CHARACTERS_PATH = "./characters/"

ZONES_INDEX_FILE = "./data/zonesindex.dat"
CREDENTIAL_FILE = "./data/credentials.dat"
ITEMS_FILE = "./data/items_common.dat"
MOBS_FILE = "./data/mobs_common.dat"

TEST_MODE = False

def configTestMode():

	print "Configuring for test mode:"
	
	global ZONES_PATH
	global ZONES_INDEX_FILE
	global CREDENTIAL_FILE
	global ITEMS_FILE
	global CHARACTERS_PATH
	global MOBS_FILE

	ZONES_PATH = "./test/zones/"
	CHARACTERS_PATH = "./test/characters/"
	ZONES_INDEX_FILE = "./test/data/zonesindex.dat"
	CREDENTIAL_FILE = "./test/data/credentials.dat"
	ITEMS_FILE = "./test/data/items_common.dat"
	MOBS_FILE = "./test/data/mobs_common.dat"

	print "zones_path      :%s" %ZONES_PATH
	print "characters_path :%s" %CHARACTERS_PATH
	print "zones_index_file:%s" %ZONES_INDEX_FILE
	print "credential_file :%s" %CREDENTIAL_FILE
	print "items_file:%s" %ITEMS_FILE
	print "mobs_file :%s" %MOBS_FILE
