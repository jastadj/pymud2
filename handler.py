import login
import game
import charcreation
import editmode
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

# character creation
client_modes.update( {"charcreation1":charcreation.charCreation}) # create char : name
client_modes.update( {"charcreation2":charcreation.charCreation}) # verify char name valid
client_modes.update( {"charcreation3":charcreation.charCreation}) # confirm name

# editor mode
client_modes.update( {"editmode1":editmode.editMenu}) # edit menu
client_modes.update( {"editmode2":editmode.editMenu}) # get selected option
client_modes.update( {"editroom1":editmode.editRoom}) # edit room menu
client_modes.update( {"editroom2":editmode.editRoom}) # edit room selection
client_modes.update( {"editroom3_1":editmode.editRoom}) # edit room name
client_modes.update( {"editroom3_2":editmode.editRoom}) # edit room name confirmation
client_modes.update( {"editroom4_1":editmode.editRoom}) # edit room desc
client_modes.update( {"editroom4_2":editmode.editRoom}) # edit room desc confirmation
client_modes.update( {"editroomdesc1":editmode.editRoomDescriptors}) # edit descriptors menu
client_modes.update( {"editroomdesc2":editmode.editRoomDescriptors}) # edit descriptors selection
client_modes.update( {"editroomdesc3_1":editmode.editRoomDescriptors}) # new descriptor val
client_modes.update( {"editroomdesc3_2":editmode.editRoomDescriptors}) # new descriptor conf
client_modes.update( {"editroomdesc3_3":editmode.editRoomDescriptors}) # new descriptor conf process
client_modes.update( {"editroomdesc4_1":editmode.editRoomDescriptors}) # check descriptor delete
client_modes.update( {"editroomdesc4_2":editmode.editRoomDescriptors}) # confirm descriptor deletion


# main modes
client_modes.update( {"maingamestart":game.mainGame}) # main game prompt
client_modes.update( {"maingame":game.mainGame}) # main game prompt

# timer update
def doTimer():
    
    if game.timer.getElapsedSec() >= 1:
        doTick()
        game.timer.reset()

def doTick():
    # update zones
    for z in game.zones:
        z.doTick()
        
    # update clients
    for u in game.clients:
        u.doTick()

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
    gameinit.gameInitTest()

    testthread = thread.start_new_thread( tickTest, () )

    def showCredentials():
        for c in game.credentials:
            print ""
            print "account name  :%s" %c.accountname
            print "account pass  :%s" %c.password
            print "character file:%s" %c.characterfile  
    
    # debug show credentials
    showCredentials()
    
    tuser = game.clients[0]
    
    doquit = False
    
    while not doquit:
        
        doTimer()
        
        handleClient(tuser)
        
        tuser.last_input = tuser.receive()
        
        if tuser.getMode() == "maingame":
            if tuser.getLastInput() == "quit" or tuser.getLastInput() == "q":
                doquit = True
            elif tuser.getLastInput() == "edit":
                tuser.setMode("editmode1")
            elif tuser.getLastInput() == "debug1":
                pass
        elif tuser.getLastInput() == "quitquit":
            doquit = True

    print "Disconnecting and saving character..."
    tuser.disconnect()
    
    #print "Saving zones..."
    #zone.saveZones()
    
    print "saving credentials..."
    credential.saveCredentials()
    
    exit()
