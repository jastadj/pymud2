import actor
import defs
import game
from tools import *

class Mob(actor.Actor):
    def __init__(self, name = "unnamed"):
        actor.Actor.__init__(self, name)


if __name__ == "__main__":
    import gameinit
    
    gameinit.gameInitTest()
    
    
