import defs
import timer
import account
import client
import testclient
import hub
import command


from tools import *

def hubinit():

    
    # load credentials
    hub.accounts = account.accountmanager()
    
    # load commands
    hub.cmds_main = command.initmaincommands()
    hub.cmds_main.setinvalidfunction( command.maingameinvalid )
        
    # timer
    hub.timer = timer.timer()
    print "Timer start:%f" %hub.timer.getstarttime()
    


def hubinittest():
    # load test configuration
    defs.TEST_MODE = True
    defs.configtestmode()
    
    hubinit()
    
    # create test user
    tuser = testclient.testclient()
    tuser.setmode("login0")
    hub.clients = []
    hub.clients.append(tuser)
    print "TestUser created..."



        


if __name__ == "__main__":
    hubinittest()
