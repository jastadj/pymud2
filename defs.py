PERS_DATA_FILE = "./data/data.dat"
ACCOUNTS_FILE = "./data/accounts.dat"
ZONES_INDEX_FILE = "./data/zonesindex.dat"
ZONES_PATH = "./zones/"
CHARACTERS_PATH = "./characters/"
ITEMS_COMMON = "./data/items_common.dat"

TEST_MODE = False

def configtestmode():

    print "Configuring for test mode:"
    
    global PERS_DATA_FILE
    global ACCOUNTS_FILE
    global ZONES_INDEX_FILE
    global ZONES_PATH
    global CHARACTERS_PATH
    global ITEMS_COMMON

    PERS_DATA_FILE = "./test/data/data.dat"
    ACCOUNTS_FILE = "./test/data/accounts.dat"
    ZONES_INDEX_FILE = "./test/data/zonesindex.dat"
    ZONES_PATH = "./test/zones/"
    CHARACTERS_PATH = "./test/characters/"
    ITEMS_COMMON = "./test/data/items_common.dat"

    print "pers data        :%s" %PERS_DATA_FILE
    print "accounts_file    :%s" %ACCOUNTS_FILE
    print "zones_index_file :%s" %ZONES_INDEX_FILE
    print "zones_path       :%s" %ZONES_PATH
    print "characters_path  :%s" %CHARACTERS_PATH
    print "items_common     :%s" %ITEMS_COMMON
