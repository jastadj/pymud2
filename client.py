import socket
import character
import game

class Client(object):
    REC_BUFFER = 4096
    
    def __init__(self):
        self.socket = None
        self.ip = None
        self.port = None
        self.credential = None
        
        self.char = None
        
        # starting user mode
        self.mode = None

        # skip next user input how many times?
        self.skip_input = 0

        # used to store temporary variables or input hist
        self.tempvars = {}
        self.last_input = ""
    
    def getAccountName(self):
        if self.credential != None:
            return self.credential.accountname
        else:
            return None
    
    def getIP(self):
        if self.ip != None:
            return self.ip
        else:
            return "No IP"
    
    def getPort(self):
        if self.port != None:
            return self.port
        else:
            return 0
    
    def setSocket(self, tsocket):
        self.socket = tsocket
    
    def getMode(self):
        return self.mode
    
    def setMode(self, tmode):
        self.mode = tmode
    
    def clearVars(self):
        self.tempvars = {}
    
    def getLastInput(self):
        return self.last_input
    
    def getVars(self):
        return self.tempvars;
        
    def setVar(self, nvar):
        self.tempvars.update(nvar)
    
    def getVar(self, key):
        try:
            return self.tempvars[key]
        except:
            return None
    
    def send(self, msg):
        if self.socket == None:
            print msg
        else:
            self.socket.send(msg);
    
    def receive(self):
        
        if self.socket == None:
            cdata = raw_input()
            return cdata
        
        # try to receivee data
        try:
            # get input from client
            cdata = self.socket.recv(Client.REC_BUFFER)
            
            # if client data valid
            if cdata:
                # trim junk from cdata
                cdata = cdata[:-2]
                self.last_input = cdata
                return cdata
            
            # else data is not valid, something happened
            # like disconnect
            else:
                self.disconnect()
         
        # client disconnected, so remove from socket list
        except:
            self.disconnect()
        
        # no valid data received, return nothing
        return None
    
    def disconnect(self):
        
        # remove client from clients list
        game.clients.remove(self)
        
        # close socket
        if self.socket != None:
            self.socket.close()
        
        # save character
        if self.credential.characterfile != None:
            print "Saving character %s to %s" %(self.char.getName() , self.credential.characterfile)
            self.char.saveToFile(self.credential.characterfile)
        else:
            print "%s's character %s : character file is null" %(self.credential.accountname, self.char.getName())
        
if __name__ == "__main__":
    
    myclient = Client()
    
