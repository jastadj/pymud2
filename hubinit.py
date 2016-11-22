import defs
import timer
import credential
import client
import testclient
import game
import command


from tools import *

def gameInit():

    
    # load credentials
    credential.loadCredentials()
    
    # load commands
    game.cmds_main = command.initMainCommands()
    game.cmds_main.setInvalidFunction( command.mainGameInvalid )
        
    # timer
    game.timer = timer.Timer()
    print "Timer start:%f" %game.timer.getStartTime()
    


def gameInitTest():
    # load test configuration
    defs.TEST_MODE = True
    defs.configTestMode()
    
    gameInit()
    
    # create test user
    tuser = testclient.TestClient()
    tuser.setMode("login0")
    game.clients = []
    game.clients.append(tuser)
    print "TestUser created..."



        


if __name__ == "__main__":
    gameInitTest()
