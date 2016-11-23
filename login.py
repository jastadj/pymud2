import hub
import character

def loginmenu(tuser):
    
    # loop through menu this many times
    dopasses = 0
    
    while dopasses >= 0:
        
        # login prompt
        if tuser.getmode() == "login0":
            tuser.send("Login:")
            tuser.setmode("login1")
        
        # check login / get password
        elif tuser.getmode() == "login1":
            
            # store login name var
            tuser.setvar({"login":tuser.getlastinput()})
            
            # new login name
            if not hub.accounts.exists(tuser.getvar("login") ):
                tuser.send("Create new account? (y/n)")
                tuser.setmode("loginnew")
                return
            
            # else, login exists, query password
            tuser.send("Password:")
            tuser.setmode("loginverify")
        
        # verify username and password
        elif tuser.getmode() == "loginverify":
            #store password var
            tuser.setvar({"password":tuser.getlastinput()})
            
            #check credential
            login = hub.accounts.dologin(tuser.getvar("login"), tuser.getvar("password"))
            
            # if login is valid
            if login != None:
                tuser.setmode("loginvalid")
                tuser.account = login
                
                print "%s logged in." %tuser.account.getuser()
                
                dopasses = 0
                continue
            # if login is NOT valid
            else:
                tuser.send("Invalid login/password!\n")
                tuser.setmode("login0")
                dopasses = 0
                continue
                
        
        # create new user query / password query
        elif tuser.getmode() == "loginnew":
            # new user confirmation, ask about new password
            try:
                if tuser.getlastinput().lower()[0] == "y":
                    tuser.send("Enter new password:")
                    tuser.setmode("loginnewpass")
                else:
                    tuser.setmode("login0")
                    continue
            # ERROR
            except:
                tuser.setmode("login0")
                dopasses = 0
                continue
        
        # new account password / verify
        elif tuser.getmode() == "loginnewpass":
            tuser.setvar({"password":tuser.getlastinput()})
            tuser.send("Enter new password again:")
            tuser.setmode("loginnewpass2")
        
        # new account password verify
        elif tuser.getmode() == "loginnewpass2":
            # if passwords do not match
            if tuser.getlastinput() != tuser.getvar("password"):
                tuser.send("Passwords do not match!\n")
                tuser.setmode("login0")
                dopasses = 1
            # else passwords match, create account
            else:
                
                # create new account and login
                hub.accounts.add(tuser.getvar("login"), tuser.getvar("password") )
                newaccount = hub.accounts.dologin( tuser.getvar("login"), tuser.getvar("password") )
                
                # account creation was successful?
                if newaccount != None:
                    
                    print "Created new user account:%s" %newaccount.getuser()
                    tuser.send("\nAccount created successfully.\n")
                    
                    # associate client with account
                    tuser.account = newaccount
                    tuser.setmode("loginvalid")
                    
                    # save accounts
                    hub.accounts.save()
                    
                    continue
                # if not, start over
                else:
                    print "Error creating user account:%s" %tuser.getvar("login")
                    tuser.setmode("login0")
                    dopasses = 1
        
        # login was valid, either create new character if necessary or goto game
        elif tuser.getmode() == "loginvalid":
            tuser.skip_input = 1
            
            if tuser.account.getcharacterfile() == None:
                tuser.setmode("createchar1")
            else:
                tuser.setmode("loadchar")
        
        elif tuser.getmode() == "loadchar":
            
            tuser.char = character.character(tuser.account)
            
            tuser.setmode("maingamestart")
            tuser.skip_input = 1
        
        
        #decrement passes
        dopasses -= 1
        

if __name__ == "__main__":
    pass
