
import credential

def loginMenu(tclient):
	
	tc = tclient
	
	# loop through menu this many times
	dopasses = 0
	
	while dopasses >= 0:
		# reprompt for login
		if tc.mode == "login0":
			tc.send("login:")
			tc.mode = "login1"
			return
		
		# login entered, get password
		elif tc.mode == "login1":
			# store login name to var1
			tc.temp_var1 = tc.last_input
			tc.send("password:")
			tc.mode = "login2"
			return
			
		# authenticate login
		elif tc.mode == "login2":
			ca = credential.credentials.getAccount({tc.temp_var1:tc.last_input})
			
			if ca == None:
				# if username exists, it was a bad login
				if credential.credentials.usernameExists(tc.temp_var1):					
					tc.send("Invalid username / pass!\n")
					tc.mode = "login0"
					dopasses = 1
				# if not, then it doesnt exists.. create a new one?
				else:
					tc.send("Create new user :%s? (y/n)" % tc.temp_var1)
					tc.mode = "loginnew"
					return
			
			# login good!
			else:
				tc.account_name = ca
				tc.mode = "maingamestart"
				tc.send("Login successful!\n")
				tc.skip_input = 1
				return
				
		# create new yser?
		elif tc.mode == "loginnew":
			try:
				if tc.last_input[0] == "y" or tc.last_input[0] == "Y":
					tc.send("Enter new password:")
					tc.mode = "loginnewpass"
					return
			except:
				pass
			
			tc.mode = "login0"
			dopasses = 1
		
		# get password reentry for checking new account
		elif tc.mode == "loginnewpass":
			tc.temp_var2 = tc.last_input
			tc.send("Enter password again:")
			tc.mode = "loginnewpass2"
			return
		
		elif tc.mode == "loginnewpass2":
			# if passwords dont match
			if tc.temp_var2 != tc.last_input:
				tc.send("Passwords do not match!\n")
				tc.mode = "login0"
				dopasses = 1
			# new user account established
			else:
				# add account
				credential.credentials.addAccount({tc.temp_var1:tc.last_input})
				
				#verify account was created and present
				na = credential.credentials.getAccount({tc.temp_var1:tc.last_input})
				if na != None:
					tc.send("New account created!\n")
					tc.account = na
					tc.mode = "maingamestart"
					tc.skip_input = 1
					return
					
				else:
					tsend("Error creating account for:%s\n" % tc.temp_var1)
					tc.mode = "login0"
					dopasses = 1
				
		
		dopasses -= 1
		

