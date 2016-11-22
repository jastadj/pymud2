import login
import game
import thread

client_modes = {}

# login modes
client_modes.update( {"login0":login.loginMenu}) # reget login
client_modes.update( {"login1":login.loginMenu}) # get password
client_modes.update( {"loginverify":login.loginMenu}) # login auth
client_modes.update( {"loginnew":login.loginMenu}) # new login query
client_modes.update( {"loginnewpass":login.loginMenu}) # new login pass verify
client_modes.update( {"loginnewpass2":login.loginMenu}) # new login pass verify
client_modes.update( {"loginvalid":login.loginMenu}) # login valid, check character

client_modes.update( {"lobby":game.lobby} ) # test lobby

# main modes
#client_modes.update( {"maingamestart":game.mainGame}) # main game prompt
#client_modes.update( {"maingame":game.mainGame}) # main game prompt

# timer update
def doTimer():
    
    if game.timer.getElapsedSec() >= 1:
        doTick()
        game.timer.reset()

def doTick():
    pass

def tickTest():
    while True:
        doTimer()

        
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
    import gameinit
    import credential
    import command
    gameinit.gameInitTest()

    testthread = thread.start_new_thread( tickTest, () )

    def showCredentials():
        for c in game.credentials:
            print ""
            print "account name  :%s" %c.accountname
            print "account pass  :%s" %c.password
    
    # debug show credentials
    showCredentials()
    
    tuser = game.clients[0]
    
    doquit = False
    
    while not doquit:
        
        doTimer()
        
        handleClient(tuser)
        
        tuser.last_input = tuser.receive()
        
        if tuser.getLastInput() == "quit":
            doquit = True

    print "Disconnecting and saving character..."
    tuser.disconnect()
    
    #print "Saving zones..."
    #zone.saveZones()
    
    print "saving credentials..."
    credential.saveCredentials()
    
    exit()
