import defs
import command
import game
import gameinit
import zone
from tools import *

def editMenu(tuser):
    # loop through menu this many times
    dopasses = 0
    
    while dopasses >= 0:
        
        # menu display / query
        if tuser.getMode() == "editmode1":
            tuser.send("\nEDIT MENU\n")
            tuser.send("---------\n")
            tuser.send("1. Edit Current Room\n")
            
            tuser.send("\n")
            tuser.send("S. Save All Changes\n")
            tuser.send("Q. Quit\n")
            
            tuser.send ("\nEDIT>")
            
            tuser.setMode("editmode2")
        
        # menu choice
        elif tuser.getMode() == "editmode2":
            if tuser.getLastInput().lower() == "q" or tuser.getLastInput().lower == "quit":
                tuser.setMode("maingame")
            elif tuser.getLastInput().lower() == "s":
                print "Saving all zones..."
                gameinit.saveZones()
                tuser.setMode("editmode1")
                continue
            elif tuser.getLastInput() == "1":
                tuser.setMode("editroom1")
                tuser.skip_input = 1
        
            
        # decrement pass
        dopasses -= 1
        
def editRoom(tuser):
    # loop through menu this many times
    dopasses = 0
    
    while dopasses >= 0:
        
        print "Zones:%d" %len(game.zones)
        print "Zone 0 rooms:%s" %len(game.zones[0].rooms)
        
        # menu display / query
        if tuser.getMode() == "editroom1":
        
            command.doLookCurrentRoom(tuser)
            
        
            tuser.send("\nEDIT ROOM\n")
            tuser.send("---------\n")
            tuser.send("1. Edit Room Name\n")
            tuser.send("2. Edit Room Description\n")
            tuser.send("3. Edit Descriptors\n")
            tuser.send("\n")
            tuser.send("B. Back\n")
            tuser.send("Q. Quit\n")
            
            tuser.send ("\nEDIT>")
            
            tuser.setMode("editroom2")
        
        # menu choice
        elif tuser.getMode() == "editroom2":
            if tuser.getLastInput().lower() == "q" or tuser.getLastInput().lower == "quit":
                tuser.setMode("maingame")
                tuser.skip_input = 1
            elif tuser.getLastInput().lower() == "b":
                tuser.setMode("editmode1")
                tuser.skip_input = 1
            elif tuser.getLastInput() == "1":
                tuser.send("Enter new room name:")
                tuser.setMode("editroom3_1")
            elif tuser.getLastInput() == "2":
                tuser.send("Enter new room description...\n:")
                tuser.setMode("editroom4_1")
            elif tuser.getLastInput() == "3":
                tuser.setMode("editroomdesc1")
                tuser.skip_input = 1
                return
        
        # edit room name confirmation #1
        elif tuser.getMode() == "editroom3_1":
            tuser.setVar({"roomname":tuser.getLastInput()})
            tuser.send("%s\n" %tuser.getVar("roomname"))
            tuser.send("Keep new room name? (y/n)")
            tuser.setMode("editroom3_2")
        
        # edit room name confirmation #2
        elif tuser.getMode() == "editroom3_2":
            if tuser.getLastInput().lower()[0] == "y":
                command.getCurrentRoom(tuser).setName(tuser.getVar("roomname"))
                tuser.clearVars()
            tuser.setMode("editroom1")
            continue
        
        # edit room description confirmation #1
        elif tuser.getMode() == "editroom4_1":
            tuser.setVar({"roomdesc":tuser.getLastInput()})
            tuser.send("%s\n" %tuser.getVar("roomdesc") )
            tuser.send("Keep new room description? (y/n)")
            tuser.setMode("editroom4_2")
        
        # edit room description confirmation #2
        elif tuser.getMode() == "editroom4_2":
            if tuser.getLastInput().lower()[0] == "y":
                command.getCurrentRoom(tuser).setDescription(tuser.getVar("roomdesc") )
                tuser.clearVars()
            tuser.setMode("editroom1")
            continue
        
        # decrement pass
        dopasses -= 1
        
def editRoomDescriptors(tuser):
    # loop through menu this many times
    dopasses = 0
    
    while dopasses >= 0:
        
        # menu display / query
        if tuser.getMode() == "editroomdesc1":
            
            troom = command.getCurrentRoom(tuser)
            tdesc = troom.getDescriptors()
            
            for d in range(0, len(tdesc.keys()) ):
                tuser.send("%d - %s:%s\n" %(d, tdesc.keys()[d], tdesc.values()[d]) )
            
        
            tuser.send("\nEDIT DESCRIPTORS\n")
            tuser.send("----------------\n")
            tuser.send("1. Add Descriptor\n")
            tuser.send("2. Delete Descriptor\n")
            tuser.send("\n")
            tuser.send("B. Back\n")
            tuser.send("Q. Quit\n")
            
            tuser.send ("\nEDIT>")
            
            tuser.setMode("editroomdesc2")
        
        ########################
        # menu choice
        elif tuser.getMode() == "editroomdesc2":
            if tuser.getLastInput().lower() == "q" or tuser.getLastInput().lower == "quit":
                tuser.setMode("maingame")
                tuser.skip_input = 1
            elif tuser.getLastInput().lower() == "b":
                tuser.setMode("editroom1")
                tuser.skip_input = 1
            elif tuser.getLastInput() == "1":
                tuser.send("Enter new descriptor key:")
                tuser.setMode("editroomdesc3_1")
            elif tuser.getLastInput() == "2":
                tuser.send("Delete descriptor #:")
                tuser.setMode("editroomdesc4_1")
            else:
                tuser.setMode("editroomdesc1")
                continue
                
        #############################        
        # add new descriptor description
        elif tuser.getMode() == "editroomdesc3_1":
            tuser.setVar({ "desckey":tuser.getLastInput()} )
            tuser.send("Enter new descriptor val:")
            tuser.setMode("editroomdesc3_2")
        # ask for new descriptor confirmation
        elif tuser.getMode() == "editroomdesc3_2":
            tuser.setVar( {"descval":tuser.getLastInput()} )
            tuser.send("New Descriptor:\n")
            tuser.send("%s:%s\n" %(tuser.getVar("desckey"), tuser.getVar("descval") ) )
            tuser.send("Keep new descriptor? (y/n)")
            tuser.setMode("editroomdesc3_3")
        # process new descriptor confirmation
        elif tuser.getMode() == "editroomdesc3_3":
            if tuser.getLastInput().lower()[0] == "y":
                # add descriptor to room
                troom = command.getCurrentRoom(tuser)
                troom.addDescriptor({tuser.getVar("desckey"):tuser.getVar("descval")} )
            tuser.clearVars()
            tuser.setMode("editroomdesc1")
            continue
        
        ####################
        # delete descriptor #
        elif tuser.getMode() == "editroomdesc4_1":
            tindex = 0
            troom = command.getCurrentRoom(tuser)
            
            try:
                tindex = int(tuser.getLastInput())
                tkey = troom.getDescriptors().keys()[tindex]
                tval = troom.getDescriptors()[tkey]
            except:
                tuser.send("Descriptor index #%s is not valid!\n" %tuser.getLastInput() )
                tuser.setMode("editroomdesc1")
                continue
            
            tuser.setVar({"tdesc":tkey})
            
            tuser.send("Descriptor #%d:\n" %tindex)
            tuser.send("%s:%s\n" %(tkey, tval) )
            tuser.send("Really delete? (y/n)")
            tuser.setMode("editroomdesc4_2")
        # confirm descriptor deletion
        elif tuser.getMode() == "editroomdesc4_2":
            troom = command.getCurrentRoom(tuser)
            if tuser.getLastInput().lower()[0] == "y":
                troom.getDescriptors().pop(tuser.getVar("tdesc"), None)
            
            tuser.setMode("editroomdesc1")
            continue
            
            
        

        
        # decrement pass
        dopasses -= 1
