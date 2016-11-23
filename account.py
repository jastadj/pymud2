import json
import defs
from tools import *

class account(object):
    def __init__(self, user, password):
        self.data = {"user":user, "password":password, "characterfile":None}
        self.data.update( {"colors":True} )

    def getuser(self):
        return self.data["user"]
        
    def getcharacterfile(self):
        return self.data["characterfile"]
    
    def colors(self):
        return self.data["colors"]
    
    def setcolors(self, docolors):
        self.data["colors"] = docolors
        
class accountmanager(object):
    
    flags = 0
    accounts = {}
    
    def __init__(self):
        
        self.load()
    
    def load(self):
        if accountmanager.flags != 0:
            return
        
        fp = defs.ACCOUNTS_FILE
        
        createNewFile(fp)
        
        with open(fp, "r") as f:
            for line in f:
                astrings = line[:-1]
                
                if astrings == "": continue
                
                jsonobj = json.loads(astrings)
                
                taccount = account("temp", "temp")
                
                taccount.data = jsonobj["data"]
                
                accountmanager.accounts.update( {taccount.getuser():taccount} )
        
        f.close()
        
        accountmanager.flags = 1
        
    def save(self):
        
        fp = defs.ACCOUNTS_FILE
        
        createNewFile(fp)
        
        f = open(fp, "w")
        
        for a in accountmanager.accounts.keys():
            
            astrings = json.dumps(accountmanager.accounts[a].__dict__)
            f.write(astrings + "\n")
        
        f.close()
        
    def add(self, user, password):
        
        if self.exists(user): return False
        
        newaccount = account(user, password)
        accountmanager.accounts.update( {newaccount.getuser():newaccount} )
    
        return True
        
    def count(self):
        
        return len(accountmanager.accounts.keys())
    
    def exists(self, user):
        
        return user in accountmanager.accounts.keys()
    
    def dologin(self, user, password):
        
        if not self.exists(user): return None
        
        if accountmanager.accounts[user].data["password"] == password:
            return accountmanager.accounts[user]
        else: return None
    
    def show(self):
        
        print "Accounts:"
        
        for a in accountmanager.accounts.keys():
            print a
        
        print "%d account(s)." %self.count()

if __name__ == "__main__":
    
    defs.configtestmode()
    
    dotest = 2
    
    acnts = accountmanager()
    
    # clear account database and create new accounts
    if dotest == 1:
        accountmanager.accounts = []
        
        acnts.addaccount("john", "monkey")
        acnts.addaccount("chong", "ler")
        
        acnts.save()

        acnts.show()
    
    # show accounts loaded from file
    elif dotest == 2:
        acnts.show()
