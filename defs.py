ACCOUNTS_FILE = "./data/accounts.dat"

TEST_MODE = False

def configtestmode():

    print "Configuring for test mode:"
    
    global ACCOUNTS_FILE

    ACCOUNTS_FILE = "./test/data/accounts.dat"

    print "accounts_file :%s" %ACCOUNTS_FILE

