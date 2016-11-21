import actor
import defs
import game
from tools import *

import command

class Mob(actor.Actor):
    def __init__(self, name = "unnamed"):
        actor.Actor.__init__(self, name)
        self.currentRoom = None
    
    def getCurrentRoom(self):
        return self.currentRoom
        
    def setCurrentRoom(self, troom):
        self.currentRoom = troom


    def doDeath(self):
        
        if self.getCurrentRoom() == None:
            print "Error doing mob death, no current room!"
            return
        
        command.broadcastToRoom(self.getCurrentRoom(), "%s dies.\n" %self.getExName() )
        
        # remove self from room
        self.currentRoom.removeMob(self)

    def setCombatTarget(self, tactor):
        self.combatTarget = tactor



if __name__ == "__main__":
    import gameinit
    
    gameinit.gameInitTest()
    
    
