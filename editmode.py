import defs
import command
import game
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
                zone.saveZones()
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
        
            tuser.send("\nEDIT ROOM\n")
            tuser.send("---------\n\n")
            command.doLookCurrentRoom(tuser)
            
            tuser.send("\n\n")
            tuser.send("1. Edit Room Name\n")
            tuser.send("2. Edit Room Description\n")
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
