import game
import character

def charCreation(tuser):
    
    # loop through menu this many times
    dopasses = 0
    
    while dopasses >= 0:
        
        if tuser.getMode() == "charcreation1":
            tuser.send("Creating new character...\n")
            tuser.setMode("maingamestart")
            
            # temp create char
            tuser.char = game.CHARACTER()
            
            # for now, just create character file as account name
            tuser.credential.characterfile = tuser.credential.accountname
            
            # for now just set character name to account name
            tuser.char.setName(tuser.credential.accountname)
            
            # save character
            character.saveCharacter(tuser.char, tuser.credential.characterfile)
            
            tuser.skip_input = 1
        
        dopasses -= 1
    
