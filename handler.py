import login
import game
import charcreation

client_modes = {}

# login modes
client_modes.update( {"login0":login.loginMenu}) # reget login
client_modes.update( {"login1":login.loginMenu}) # get password
client_modes.update( {"loginverify":login.loginMenu}) # login auth
client_modes.update( {"loginnew":login.loginMenu}) # new login query
client_modes.update( {"loginnewpass":login.loginMenu}) # new login pass verify
client_modes.update( {"loginnewpass2":login.loginMenu}) # new login pass verify
client_modes.update( {"loginvalid":login.loginMenu}) # login valid, check character

# character creation
client_modes.update( {"charcreation1":charcreation.charCreation}) # create char : name

# main modes
client_modes.update( {"maingamestart":game.mainGame}) # main game prompt
client_modes.update( {"maingame":game.mainGame}) # main game prompt

def handleClient(tclient):
    
    cc = tclient.getLastInput()
    
    # run loop, skipping input if set
    while tclient.skip_input >= 0:
    
        # client output, goto client mode function pointer
        client_modes[ tclient.mode ](tclient)
        
        # client input
        if cc == "quit":
            tclient.disconnect()
        
        # decrement input skip for next pass
        if tclient.skip_input != 0:
            tclient.last_input = ""
            
        # decrement skip input
        tclient.skip_input -= 1
    
    # reset input skip counter
    tclient.skip_input = 0

if __name__ == "__main__":
    import defs
    import credential
    import testclient
    import game
    import item
    import room
    import zone
    import command
    import character
    
    # load test configuration
    defs.configTestMode()


    # callbacks
    game.ITEM = item.Item
    game.ROOM = room.Room
    game.ZONE = zone.Zone
    game.COMMAND = command.Command
    game.COMMAND_SET = command.CommandSet
    game.CHARACTER = character.Character

    # load credentials
    credential.loadCredentials()

    # load commands
    game.cmds_main = command.initMainCommands()
    game.processnoncmd = command.processNonCommand
    
    # load items
    item.loadItems()

    # load zones
    zone.loadZones()
        
    def showCredentials():
        for c in game.credentials:
            print ""
            print "account name  :%s" %c.accountname
            print "account pass  :%s" %c.password
            print "character file:%s" %c.characterfile  
    
    # debug show credentials
    showCredentials()
    
    # create test user
    tuser = testclient.TestClient()
    tuser.setMode("login0")
    game.clients = []
    game.clients.append(tuser)

    doquit = False

    
    while not doquit:
        
        handleClient(tuser)
        
        tuser.last_input = tuser.receive()
        
        if tuser.getLastInput() == "quit":
            doquit = True

    print "Disconnecting and saving character..."
    tuser.disconnect()
    
    print "saving credentials..."
    credential.saveCredentials()
    
    
