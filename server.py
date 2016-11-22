import socket, select
import account
import client
import handler
import hubinit
import hub
from tools import *

class server(object):
    def __init__(self):
                
        self.socket = None
        #0=uninit, 1=initialized, -1=shutdown
        self.status = 0 
        
    def isrunning(self):
        if self.status == 1:
            return True
        else: return False
    
    def initserver(self):
        
        if self.isrunning():
            print "Unable to start server!"
            return False

        print "Starting server..."
        self.status = 1
        
        #create an INET, STREAMing socket
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        
        # bind locally on port
        self.socket.bind( ("0.0.0.0", 8888) )
        
        # listed on socket
        self.socket.listen(5)
        
        print "Socket is listening..."
        
        # init main game
        hubinit.hubinit()
        
        return True
        
    def getallsockets(self):
        
        if not self.isrunning():
            print "Unable to get all sockets, server is not running!"
            return None
        
        # socket list
        slist = []
        
        # add server socket
        slist.append(self.socket)

        
        # add all client sockets
        for u in hub.clients:
            print u
            slist.append( u.socket)
        
        return slist

    def getclient(self, tsocket):
        
        # look and return client with target socket
        for tclient in hub.clients:
            if tsocket == tclient.socket:
                return tclient
        
        # not found, return None
        return None

    def mainloop(self):
        
        while self.isrunning():
            
            try:
                read_sockets,write_sockets,error_sockets = select.select( self.getallsockets(),[],[], 0)
            except:
                print "Selector failed to read."
                continue
            
            handler.dotimer()
            
            for tsock in read_sockets:
                
                # if server has something to do (new connection?)
                if tsock == self.socket:
                    
                    # get accepted new connection socket
                    newsock, addr = self.socket.accept()
                    
                    # create new client
                    newclient = client.client()
                    newclient.setsocket(newsock)
                    newclient.ip = addr[0]
                    newclient.port = addr[1]
                    
                    # add new client to list
                    game.clients.append(newclient)
                    print "Client %s:%d connected." %(newclient.getip(), newclient.getport())
                    
                    #print WELCOME screen
                    newclient.send("\n#c2Welcome!#cr\n\n")
                    
                    # configure client starting mode
                    newclient.setmode("login1")
                    newclient.send("login:")
                
                # else a client has something to do
                else:
                    
                    tclient = self.getclient(tsock)
                    
                    if tclient == None:
                        print "Error finding client with target socket!"
                        print "Closing socket..."
                        tsock.close()
                        continue
                            
                    # receive client data
                    cdata = tclient.receive()
                    
                    # if unable to receive data, something went wrong
                    if cdata == None:
                        # remove client from list
                        print "Client %s:%d disconnected." %(tclient.ip, tclient.port)
                        game.clients.remove(tclient)
                        continue
                    
                    # debug
                    if cdata == "shutdown":
                        tclient.send("Commanded server shutdown.\n")
                        self.status = -1
                    
                    # input is valid
                    # now give client feedback
                    handler.handleclient(tclient)
                    
                    
            

    def shutdownserver(self):           
        
        print "Shutting down server..."
        
        if self.status != -1:
            self.status = -1
        
        
        # save stuff
        hub.accounts.saveaccounts()
        print "Accounts saved."
        
        # shutdown and close server socket
        self.socket.shutdown(0)
        self.socket.close()
        self.socket = None

        
        return True




if __name__ == "__main__":
    testserver = server()
    testserver.initserver()
    testserver.shutdownserver()
