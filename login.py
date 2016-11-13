
import credential
import character

def loginMenu(tuser):
    
    # loop through menu this many times
    dopasses = 0
    
    while dopasses >= 0:
        
        # login prompt
        if tuser.getMode() == "login0":
            tuser.send("Login:")
            tuser.setMode("login1")
        
        # check login / get password
        elif tuser.getMode() == "login1":
            
            if not character.validCharacterName(tuser.getLastInput()):
                tuser.send("That is not a valid user name!  (Letters only, no spaces!)\n")
                tuser.setMode("login0")
                dopasses = 0
                continue
            
            # store login name var
            tuser.setVar({"login":tuser.getLastInput()})
            
            # new login name
            if credential.accountNameAvailable(tuser.getVar("login") ):
                tuser.send("Create new account? (y/n)")
                tuser.setMode("loginnew")
                return
            
            # else, login exists, query password
            tuser.send("Password:")
            tuser.setMode("loginverify")
        
        # verify username and password
        elif tuser.getMode() == "loginverify":
            #store password var
            tuser.setVar({"password":tuser.getLastInput()})
            
            #check credential
            login = credential.doLogin(tuser.getVar("login"), tuser.getVar("password"))
            
            # if login is valid
            if login != None:
                tuser.setMode("loginvalid")
                tuser.credential = login
                dopasses = 0
                continue
            # if login is NOT valid
            else:
                tuser.send("Invalid login/password!\n")
                tuser.setMode("login0")
                dopasses = 0
                continue
                
        
        # create new user query / password query
        elif tuser.getMode() == "loginnew":
            # new user confirmation, ask about new password
            try:
                if tuser.getLastInput()[0] == "y" or tuser.getLastInput()[0] == "Y":
                    tuser.send("Enter new password:")
                    tuser.setMode("loginnewpass")
                else:
					tuser.setMode("login0")
					continue
            # ERROR
            except:
                tuser.setMode("login0")
                dopasses = 0
                continue
        
        # new account password / verify
        elif tuser.getMode() == "loginnewpass":
            tuser.setVar({"password":tuser.getLastInput()})
            tuser.send("Enter new password again:")
            tuser.setMode("loginnewpass2")
        
        # new account password verify
        elif tuser.getMode() == "loginnewpass2":
            # if passwords do not match
            if tuser.getLastInput() != tuser.getVar("password"):
                tuser.send("Passwords do not match!\n")
                tuser.setMode("login0")
                dopasses = 1
            # else passwords match, create account
            else:
                # create new account
                newaccount = credential.addNewAccount( tuser.getVar("login"), tuser.getVar("password") )
                
                # account creation was successful?
                if newaccount != None:
                    tuser.credential = newaccount
                    tuser.setMode("loginvalid")
                    continue
                # if not, start over
                else:
                    print "Error creating user account:%s" %tuser.getVar("login")
                    tuser.setMode("login0")
                    dopasses = 1
        
        # login was valid, either create new character if necessary or goto game
        elif tuser.getMode() == "loginvalid":
            
            # if character file, load character
            if tuser.credential.characterfile != None:
                
                # attempt to load character file
                tuser.char = character.loadCharacter(tuser.credential.characterfile)
                
                # if no character file, create new character
                if tuser.char == None:
                    print "Error loading character, creating new..."
                    tuser.skip_input = 1
                    tuser.setMode("charcreation1")
                
                # character loaded, enter game
                else:
                    tuser.setMode("maingamestart")
                    tuser.skip_input = 1
            
            # no characer file, create character
            else:
                tuser.skip_input = 1
                tuser.setMode("charcreation1")
				
        
        
        #decrement passes
        dopasses -= 1
        

if __name__ == "__main__":
	pass
