from tools import *
import defs
import game

class Credential(object):
    def __init__(self, accountname, password, characterfile):
        self.accountname = accountname
        self.password = password
        self.characterfile = characterfile

def accountNameAvailable(accountname):
	
	for c in game.credentials:
		if c.accountname == accountname:
			return False
	
	return True

def addNewAccount(accountname, password):
	if not accountNameAvailable(accountname):
		print "Error adding new account %s, name not available!" %accountname
		return None
	
	newaccount = Credential(accountname, password, None)
	game.credentials.append(newaccount)
	
	print "New account created for:%s" %accountname
	
	return newaccount

def doLogin(accountname, password):
	
	tcred = None
	
	# check credentials for account name
	for c in game.credentials:
		if accountname == c.accountname:
			tcred = c
	
	# no account name found
	if tcred == None:
		return None
		
	# check password match, return credential
	if tcred.password == password:
		return tcred
	
	# no matching name/pass found
	return None
		

def loadCredentials():
    
    fp = defs.CREDENTIAL_FILE
    
    game.credentials = []
    
    #print "LOADING CREDENTIALS FROM %s" %fp
    
    # if file already exists
    if createNewFile(fp) == None:
        
        # check each line in credential file
        with open(fp, "r") as f:
            for line in f:
                # trim off newline
                line = line[:-1]
                
                #ignore blank lines
                if line == "":
                    continue
                
                # if account entry
                if line.startswith("ACCOUNT:"):
                    
                    # find delmiter, trip off entry type
                    dfind = line.find(':')
                    line = line[dfind+1:]
                    
                    # get account name
                    cfind = line.find(',')
                    aname = line[:cfind]
                    line = line[cfind+1:]
                    
                    # get account password
                    cfind = line.find(',')
                    apass = line[:cfind]
                    line = line[cfind+1:]
                    
                    # get account character file
                    acharfile = line
                    if acharfile == "None":
						acharfile = None
                    
                    # create credential
                    game.credentials.append(Credential(aname, apass, acharfile))
        f.close()
                    

def saveCredentials():
    
    fp = defs.CREDENTIAL_FILE
    
    createNewFile(fp)
    
    f = open(fp, "w")
    
    for c in game.credentials:
        f.write("ACCOUNT:%s,%s,%s\n" %(c.accountname, c.password, c.characterfile) )
    
    f.close()

if __name__ == "__main__":
    
    defs.configTestMode()
    
    def showCredentials():
        for c in game.credentials:
            print ""
            print "account name  :%s" %c.accountname
            print "account pass  :%s" %c.password
            print "character file:%s" %c.characterfile
    
    # create test credentials
    game.credentials = []
    game.credentials.append(Credential("john", "monkey", "billy.dat") )
    game.credentials.append(Credential("j","j","j.dat") )
    
    # save credentials
    saveCredentials()
    
    # clear game credentials
    game.credentials = []
    
    # load game credentials
    loadCredentials()
    
    showCredentials()  
    
