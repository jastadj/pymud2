import login
import createchar
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
client_modes.update( {"loadchar":login.loginmenu}) # all is good, load character file

client_modes.update( {"createchar1":createchar.createchar}) # create character
client_modes.update( {"createchar2":createchar.createchar}) # check char name validity
client_modes.update( {"createchar3":createchar.createchar}) # check keep confirmation

client_modes.update( {"lobby":hub.lobby} ) # test lobby

# main modesj
client_modes.update( {"maingamestart":hub.maingame}) # main game prompt
client_modes.update( {"maingame":hub.maingame}) # main game prompt


client_modes.update( {"disconnected":hub.disconnected}) # disconnect mode

# timer update
def dotimer():
    if hub.timer.getelapsedsec() >= 2:
        dotick()
        hub.timer.reset()


def dotick():

    hub.mainmutex.acquire()
    
    try:
        # update all rooms
        for r in hub.worldobjects_specific["room"].keys():
            hub.worldobjects[r].dotick()
        
        # update players for combat
        for u in hub.clients:
            if u.char != None:
                u.char.dotick()
    finally:
        hub.mainmutex.release()

def ticktest():
    while True:
        
        dotimer()

        
def handleclient(tclient):
    
    hub.mainmutex.acquire()
    
    try:
        
        cc = tclient.getlastinput()
        
        # run loop, skipping input if set
        while tclient.skip_input >= 0:
        
            # client output, goto client mode function pointer
            client_modes[ tclient.mode ](tclient)
            
            # decrement input skip for next pass
            if tclient.skip_input != 0:
                tclient.last_input = ""
                
            # decrement skip input
            tclient.skip_input -= 1
        
        # reset input skip counter
        tclient.skip_input = 0
    
    finally:
        hub.mainmutex.release()

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
        
        tuser.send("\n")
        
        if tuser.getlastinput() == "quit":
            doquit = True

    print "Disconnecting and saving character..."
    tuser.disconnect()
    
    if tuser.char != None:
        tuser.char.save()
    
    hubinit.save()
    
    exit()
