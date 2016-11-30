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
        
    def todict(self):
        tdict = {"data":self.data}
        return tdict
    
    def toJSONstr(self):
        return json.dumps( self.todict() )
    
    def fromJSON(self, jobj):
        
        self.data = jobj["data"]
        
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
        
        f = open(fp, "r")
        
        jstrings = f.read()
        
        if jstrings != "":
        
            jsonobj = json.loads(jstrings)
            
            self.fromJSON(jsonobj)
        
        f.close()
        
        accountmanager.flags = 1
        
    def save(self):
        
        fp = defs.ACCOUNTS_FILE
        
        createNewFile(fp)
        
        f = open(fp, "w")
        
        f.write( self.toJSONstr() )
        
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
    
    def todict(self):
        
        tdict = {"accounts":{} }
        
        for a in accountmanager.accounts.keys():
            
            tdict["accounts"].update( { a : accountmanager.accounts[a].todict() } )
        
        return tdict
    
    def toJSONstr(self):
        
        return json.dumps( self.todict() )
        
    def fromJSON(self, jobj):
        
        for a in jobj["accounts"].keys():
            taccount = account("test","test")
            taccount.fromJSON( jobj["accounts"][a])
            accountmanager.accounts.update( {taccount.getuser():taccount} )
    
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
        accountmanager.accounts = {}
        
        acnts.add("john", "monkey")
        acnts.add("chong", "ler")
        
        acnts.save()

        acnts.show()
    
    # show accounts loaded from file
    elif dotest == 2:
        acnts.show()
