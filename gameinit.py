import defs
import credential
import testclient
import game
import item
import room
import zone
import command
import character
import weapon
import armor
import mob


def gameInit():

    # game callbacks
    game.ITEM = item.Item
    game.WEAPON = weapon.Weapon
    game.ARMOR = armor.Armor
    
    game.ROOM = room.Room
    game.ZONE = zone.Zone

    game.COMMAND = command.Command
    game.COMMAND_SET = command.CommandSet

    game.CHARACTER = character.Character
    game.MOB = mob.Mob
    
    #zero lists
    game.items = []
    
    # load credentials
    credential.loadCredentials()
	
    # load commands
    game.cmds_main = command.initMainCommands()
    game.cmds_main.setInvalidFunction( command.mainGameInvalid )
    
    
    # load items
    item.loadItems()

    # load mobs
    mob.loadMobs()
    
    # load zones
    zone.loadZones()
    
    # feedback
    print "%d accounts loaded." %len(game.credentials)
    print "%d commands loaded." %len(game.cmds_main.commands)    
    print "%d items loaded." %len(game.items)
    print "%d mobs loaded." %len(game.mobs)
    print "%d zones loaded." %len(game.zones)
	


def gameInitTest():
    # load test configuration
    defs.configTestMode()
    
    gameInit()
    
    # create test user
    tuser = testclient.TestClient()
    tuser.setMode("login0")
    game.clients = []
    game.clients.append(tuser)
    print "TestUser created..."
    
if __name__ == "__main__":
    gameInitTest()