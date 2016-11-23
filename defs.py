ACCOUNTS_FILE = "./data/accounts.dat"
ZONES_INDEX_FILE = "./data/zonesindex.dat"
ZONES_PATH = "./zones/"
CHARACTERS_PATH = "./characters/"
TEST_MODE = False

def configtestmode():

    print "Configuring for test mode:"
    
    global ACCOUNTS_FILE
    global ZONES_INDEX_FILE
    global ZONES_PATH
    global CHARACTERS_PATH

    ACCOUNTS_FILE = "./test/data/accounts.dat"
    ZONES_INDEX_FILE = "./test/data/zonesindex.dat"
    ZONES_PATH = "./test/zones/"
    CHARACTERS_PATH = "./test/characters/"

    print "accounts_file    :%s" %ACCOUNTS_FILE
    print "zones_index_file :%s" %ZONES_INDEX_FILE
    print "zones_path       :%s" %ZONES_PATH
    print "characters_path  :%s" %CHARACTERS_PATH
