PERS_DATA_FILE = "./data/data.dat"
ACCOUNTS_FILE = "./data/accounts.dat"
ZONES_INDEX_FILE = "./data/zonesindex.dat"
ZONES_PATH = "./zones/"
CHARACTERS_PATH = "./characters/"
ITEMS_COMMON = "./data/items_common.dat"
MOBS_COMMON = "./data/mobs_common.dat"

TEST_MODE = False


# BODY PARTS
BODYPART_HEAD = 0
BODYPART_NECK = 1
BODYPART_TORSO = 2
BODYPART_LEFTARM = 3
BODYPART_RIGHTARM = 4
BODYPART_LEFTHAND = 5
BODYPART_RIGHTHAND = 6
BODYPART_WAIST = 7
BODYPART_LEFTLEG = 8
BODYPART_RIGHTLEG = 9
BODYPART_LEFTFOOT = 10
BODYPART_RIGHTFOOT = 11

def configtestmode():

    print "Configuring for test mode:"
    
    global PERS_DATA_FILE
    global ACCOUNTS_FILE
    global ZONES_INDEX_FILE
    global ZONES_PATH
    global CHARACTERS_PATH
    global ITEMS_COMMON
    global MOBS_COMMON

    PERS_DATA_FILE = "./test/data/data.dat"
    ACCOUNTS_FILE = "./test/data/accounts.dat"
    ZONES_INDEX_FILE = "./test/data/zonesindex.dat"
    ZONES_PATH = "./test/zones/"
    CHARACTERS_PATH = "./test/characters/"
    ITEMS_COMMON = "./test/data/items_common.dat"
    MOBS_COMMON = "./test/data/mobs_common.dat"

    print "pers data        :%s" %PERS_DATA_FILE
    print "accounts_file    :%s" %ACCOUNTS_FILE
    print "zones_index_file :%s" %ZONES_INDEX_FILE
    print "zones_path       :%s" %ZONES_PATH
    print "characters_path  :%s" %CHARACTERS_PATH
    print "items_common     :%s" %ITEMS_COMMON
    print "mobs_common      :%s" %MOBS_COMMON
