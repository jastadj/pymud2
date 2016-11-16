import game
import character
import defs
from tools import *

def charCreation(tuser):
    
    # loop through menu this many times
    dopasses = 0
    
    while dopasses >= 0:
        
        if tuser.getMode() == "charcreation1":
            tuser.send("Creating new character...\n")
            tuser.send("Enter character name: >")
            tuser.setMode("charcreation2")
            #tuser.setMode("maingamestart")
            
            # temp create char
            #tuser.char = game.CHARACTER()
            
            # for now, just create character file as account name
            #tuser.credential.characterfile = tuser.credential.accountname
            
            # for now just set character name to account name
            #tuser.char.setName(tuser.credential.accountname)
            
            # save character
            #character.saveCharacter(tuser.char, tuser.credential.characterfile)
            
            #tuser.skip_input = 1
        
        # verify char name is valid
        elif tuser.getMode() == "charcreation2":
            tname = tuser.getLastInput()
            tuser.setVar( {"charname":tuser.getLastInput() } )
            
            # if char already exists
            if fileExists( defs.CHARACTERS_PATH + "%s.dat" %tname):
                tuser.send("That name is already in use!\n")
                tuser.setMode("charcreation1")
                continue
            
            if not character.validCharacterName(tname):
                tuser.send("That name is not valid!  Letters only, no spaces.\n")
                tuser.setMode("charcreation1")
                continue
            
            tuser.send("Are you sure you want to be named '%s'? (y/n)" %tname)
            tuser.setMode("charcreation3")
        
        # verify chosen name
        elif tuser.getMode() == "charcreation3":
            if tuser.getLastInput().lower()[0] != "y":
                tuser.setMode("charcreation1")
                continue
            
            # create character
            tuser.char = game.CHARACTER()
            tuser.credential.characterfile = "%s.dat" %tuser.getVar("charname")
            tuser.char.setName(tuser.getVar("charname"))
            
            # save character
            character.saveCharacter(tuser.char, tuser.credential.characterfile)
            
            #done
            tuser.setMode("maingamestart")
            tuser.skip_input = 1
        
        dopasses -= 1
    
