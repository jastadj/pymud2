import game

def charCreation(tuser):
    
    # loop through menu this many times
    dopasses = 0
    
    while dopasses >= 0:
        
        if tuser.getMode() == "charcreation1":
            tuser.send("Creating new character...\n")
            tuser.setMode("maingamestart")
            
            # temp create char
            tuser.char = game.CHARACTER()
            
            tuser.skip_input = 1
        
        dopasses -= 1
    
