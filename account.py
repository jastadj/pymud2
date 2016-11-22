import json
import defs
from tools import *

class account(object):
    def __init__(self, user, password):
        self.data = {"user":user, "password":password}

    def getuser(self):
        return self.data["user"]
        
class accountmanager(object):
    
    flags = 0
    accounts = []
    
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
                
                accountmanager.accounts.append(taccount)
        
        f.close()
        
        accountmanager.flags = 1
        
    def save(self):
        
        fp = defs.ACCOUNTS_FILE
        
        createNewFile(fp)
        
        f = open(fp, "w")
        
        for a in accountmanager.accounts:
            
            astrings = json.dumps(a.__dict__)
            f.write(astrings + "\n")
        
        f.close()
        
    def add(self, user, password):
        
        newaccount = account(user, password)
        accountmanager.accounts.append(newaccount)
    
    def count(self):
        
        return len(accountmanager.accounts)
    
    def exists(self, user):
        
        for a in accountmanager.accounts:
            if user == a.getuser(): return True
        
        return False
    
    def dologin(self, user, password):
        
        for a in accountmanager.accounts:
            if user == a.getuser():
                if a.data["password"] == password:
                    return a
                else: return None
        
        return None
    
    def show(self):
        
        print "Accounts:"
        
        for a in accountmanager.accounts:
            print a.getuser()
        
        print "%d account(s)." %self.count()

if __name__ == "__main__":
    
    defs.configTestMode()
    
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
