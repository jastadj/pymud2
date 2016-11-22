import login
import hub
import thread

client_modes = {}

# login modes
client_modes.update( {"login0":login.loginmenu}) # reget login
client_modes.update( {"login1":login.loginmenu}) # get password
client_modes.update( {"loginverify":login.loginmenu}) # login auth
client_modes.update( {"loginnew":login.loginmenu}) # new login query
client_modes.update( {"loginnewpass":login.loginmenu}) # new login pass verify
client_modes.update( {"loginnewpass2":login.loginmenu}) # new login pass verify
client_modes.update( {"loginvalid":login.loginmenu}) # login valid, check character

client_modes.update( {"lobby":hub.lobby} ) # test lobby

# main modes
#client_modes.update( {"maingamestart":game.mainGame}) # main game prompt
#client_modes.update( {"maingame":game.mainGame}) # main game prompt

# timer update
def dotimer():
    
    if hub.timer.getelapsedsec() >= 1:
        dotick()
        hub.timer.reset()

def dotick():
    pass

def ticktest():
    while True:
        dotimer()

        
def handleclient(tclient):
    
    cc = tclient.getlastinput()
    
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
    import hubinit
    import account
    import command
    
    hubinit.hubinittest()

    testthread = thread.start_new_thread( ticktest, () )

    hub.accounts.show()
    
    
    tuser = hub.clients[0]
    
    doquit = False
    
    while not doquit:
        
        dotimer()
        
        handleclient(tuser)
        
        tuser.last_input = tuser.receive()
        
        if tuser.getlastinput() == "quit":
            doquit = True

    print "Disconnecting and saving character..."
    tuser.disconnect()
    
    #print "Saving zones..."
    #zone.saveZones()
    
    print "saving accounts..."
    hub.accounts.save()
    
    exit()
