import socket
import hub
from tools import *

class client(object):
    REC_BUFFER = 4096

    def __init__(self):
        self.socket = None
        self.ip = None
        self.port = None
        self.account = None

        self.char = None

        # starting user mode
        self.mode = None

        # skip next user input how many times?
        self.skip_input = 0

        # used to store temporary variables or input hist
        self.tempvars = {}
        self.last_input = ""

    def getaccountname(self):
        if self.account != None:
            return self.account.getuser()
        else:
            return None

    def getip(self):
        if self.ip != None:
            return self.ip
        else:
            return "No IP"

    def getport(self):
        if self.port != None:
            return self.port
        else:
            return 0

    def setsocket(self, tsocket):
        self.socket = tsocket

    def getmode(self):
        return self.mode

    def setmode(self, tmode):
        self.mode = tmode

    def clearvars(self):
        self.tempvars = {}

    def getlastinput(self):
        return self.last_input

    def getvars(self):
        return self.tempvars;

    def setvar(self, nvar):
        self.tempvars.update(nvar)

    def getvar(self, key):
        try:
            return self.tempvars[key]
        except:
            return None

    def colors(self):
        if self.account != None:
            return self.account.colors()
        else: return True

    def processcolors(self, msg):

        # get message range to iterate through
        mlen = len(msg)

        newmsg = ""

        if mlen < 3: return msg

        doskip = 0

        # find color code in msg string
        for i in range(0, mlen):


            # color code found
            if msg[i] == '#' and i + 2 < mlen:

                tbold = False
                tcolor = 0

                if msg[i+1] == 'C':
                    tbold = True

                tcolor = msg[i+2]
                
                if self.colors():
                
                    # reset code
                    if tcolor.lower() == "r":
                        newmsg += resetColor()

                    else:
                        try:
                            tcolor = int(tcolor)
                            newmsg += setColor(tcolor, tbold)
                        except:
                            pass

                # advance iterator
                doskip = 2


            else:
                if doskip != 0:
                    doskip -= 1
                else:
                    # add character to new message
                    newmsg += msg[i]


        return newmsg

    def send(self, msg):

        msg = self.processcolors(msg)

        if self.socket == None:
            print msg
        else:
            self.socket.send(msg);

    def dotick(self):
        if self.char != None:
            self.char.doTick()

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

    def disconnect(self):

        # remove client from clients list
        hub.clients.remove(self)

        # close socket
        if self.socket != None:
            self.socket.close()


if __name__ == "__main__":

    myclient = client()
    myclient.send("#c1This is #c2a#cr test!")
