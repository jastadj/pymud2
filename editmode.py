import defs
import command
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
            tuser.send("Q. Quit\n")
            
            tuser.send ("\nEDIT>")
            
            tuser.setMode("maingame")
        
        # menu choice
        elif tuser.getMode() == "editmode2":
            if tuser.getLastInput().lower() == "q" or tuser.getLastInput().lower == "quit":
                tuser.setMode("maingame")
            elif tuser.getLastInput() == "1":
                tuser.setMode("editroom1")
                tuser.skip_input = 1
        
            
        # decrement pass
        dopasses -= 1
        
def editRoom(tuser):
    # loop through menu this many times
    dopasses = 0
    
    while dopasses >= 0:
        
        # menu display / query
        if tuser.getMode() == "editroom1":
        
            tuser.send("\nEDIT ROOM\n")
            tuser.send("---------\n\n")
            command.doLookCurrentRoom(tuser)
            
            tuser.send("\n\n")
            tuser.send("1. Edit Room Name\n")
            tuser.send("\n")
            tuser.send("B. Back\n"
            tuser.send("Q. Quit\n")
            
            tuser.send ("\nEDIT>")
            
            tuser.setMode("editroom2")
        
        # menu choice
        elif tuser.getMode() == "editmode2":
            if tuser.getLastInput().lower() == "q" or tuser.getLastInput().lower == "quit":
                tuser.setMode("maingame")
                tuser.skip_input = 1
            elif tuser.getLastInput().lower() == "b":
                tuser.setMode("editmode1")
                tuser.skip_input = 1
            elif tuser.getLastInput() == "1":
                tuser.send("Enter new room name:")
                tuser.setMode("editroom3_1")
                continue
        
        elif tuser.getMode() == "editmode3_1":
            tuser.setVar({"roomname":tuser.getLastInput()})
            asfasf
        
            
        # decrement pass
        dopasses -= 1