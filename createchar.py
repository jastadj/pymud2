import defs
import character
from tools import *

def createchar(tuser):
    
    # loop through menu this many times
    dopasses = 0
    
    while dopasses >= 0:
        
        # new character name
        if tuser.getmode() == "createchar1":
            tuser.send("New character name:")
            tuser.setmode("createchar2")
        
        # check char name valid / confirmation
        elif tuser.getmode() == "createchar2":
            
            cname = tuser.getlastinput()
            
            # check that name is valid
            for c in cname:
                if c < "a" or c > "z":
                    if c < "A" or c > "Z":
                        tuser.send("That name is not valid, characters only, no spaces!\n")
                        tuser.setmode("createchar1")
                        continue
            
            # check that character name has not already been picked
            if fileExists( defs.CHARACTERS_PATH + cname + ".dat" ):
                tuser.send("That name already exists!  Please choose a different name.\n")
                tuser.setmode("createchar1")
                continue
            
            
            # format name
            tempname = ""
            tempname += cname[0].upper()
            tempname += cname[1:].lower()
            cname = tempname
            
            
            
            # character name is availalble, prompt confirmation
            tuser.send("You will be known as %s, create this character? (y/n)" %cname)
            tuser.setvar( {"charname":cname} )
            tuser.setmode("createchar3")
            
        elif tuser.getmode() == "createchar3":
            if tuser.getlastinput().lower()[0] == "y":
                # create character
                tuser.account.data["characterfile"] = tuser.getvar("charname") + ".dat"
                tuser.char = character.character(tuser.account, tuser.getvar("charname"))
                tuser.setmode("loadchar")
                tuser.skip_input = 1
            else:
                tuser.setmode("createchar1")
                continue

        
        #decrement passes
        dopasses -= 1
