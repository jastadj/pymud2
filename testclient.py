from __future__ import print_function
import client

class testclient(client.client):
        REC_BUFFER = 4096
        
        def __init__(self):
                client.client.__init__(self)
        
        def send(self, msg):
                
                msg = self.processcolors(msg)
                
                if self.socket == None:
                        print(msg, end="")
                else:
                        self.socket.send(msg);
        
        def receive(self):
                
                if self.socket == None:
                        cdata = raw_input()
                        return cdata
                
                # try to receivee data
                try:
                        # get input from client
                        cdata = self.socket.recv(client.REC_BUFFER)
                        
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
                
if __name__ == "__main__":
        
        myclient = testclient()
        
        myclient.send("#c1THIS IS A TEST!#cr")

