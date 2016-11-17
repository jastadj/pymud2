if __name__ == "__main__":
    import gameinit
    import game
    
    import item
    import mob
    import zone
    import credential
    import character
    gameinit.gameInitTest()
    
    print "\nGenerating test data...\n"
    
    #####
    # ITEMS
    #####
    game.items_common = []
    newitem = game.ITEM("rock")
    game.items_common.append(newitem)
    

    #####
    newitemweapon = game.WEAPON("sword")
    newitemweapon.noun.addAdjective("long")
    newitemweapon.setDescription("A pretty sharp looking sword.")
    newitemweapon.setDamage(3)
    game.items_common.append(newitemweapon)
    
    #####
    newitemweapon2 = game.WEAPON("axe")
    newitemweapon2.noun.addAdjective("battle")
    newitemweapon2.setDescription("A grisly looking battle axe")
    newitemweapon2.setDamage(5)
    newitemweapon2.setHands(2)
    game.items_common.append(newitemweapon2)
    
    #####
    newitemarmor = game.ARMOR("cap")
    newitemarmor.noun.addAdjective("leather")
    newitemarmor.setDescription("A cap made out of boiled leather.")
    newitemarmor.setSlotUsed("head")
    game.items_common.append(newitemarmor)
    
    print "Saving items to file..."
    item.saveItems()
    
    #####
    # MOBS
    #####
    
    #####
    mob1 = game.MOB("Billy")    
    game.mobs.append(mob1)
    
    # save mob file
    print "Saving mobs to file..."
    mob.saveMobs()
        
    #####
    # ZONES
    #####
    
    #####
    newzone = game.ZONE("Billy's Apartment")
    newzone.setDescription("A pretty plain apartment.")
    newzone.zonefile = "apartment.zn"
    
    #####
    bathroom = game.ROOM("Bathroom")
    bathroom.setDescription("You are standing in a bathroom that doesn't look like it has been maintained for some time.  The smells of stale urine fills your nose.  A grungry sink hangs precariously from the tiled wall.")
    bathroom.addExit("north", 1)
    bathroom.addNewItem("sword")
    newzone.addRoom(bathroom)
    
    #####
    livingroom = game.ROOM("Living Room")
    livingroom.setDescription("A pretty boring living room vacant of furniture.  Old posters are pinned lazily to the wall.")
    livingroom.addExit("south", 0)
    newzone.addRoom(livingroom)
    
    game.zones = []
    game.zones.append(newzone)
    
    # save test zones
    print "Saving zones to file..."
    zone.saveZones()    
    
    #####
    # ACCOUNT
    #####
    game.credentials = []
    newcredential = credential.Credential("j","j","cholo.dat")
    game.credentials.append(newcredential)
    newchar = character.Character()
    newchar.setName("Cholo")
    print "Saving credential and char..."
    credential.saveCredentials()
    character.saveCharacter(newchar, "cholo.dat")
    
    #####
    print "\nTest data done."
