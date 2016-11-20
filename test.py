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
    newitem = game.OBJECT_CLASSES["Item"]("rock")
    game.items_common.append(newitem)
    

    #####
    newitemweapon = game.OBJECT_CLASSES["Weapon"]("sword")
    newitemweapon.addAdjective("long")
    newitemweapon.setDescription("A pretty sharp looking sword.")
    newitemweapon.setDamage(3)
    game.items_common.append(newitemweapon)
    
    #####
    newitemweapon2 = game.OBJECT_CLASSES["Weapon"]("axe")
    newitemweapon2.addAdjective("battle")
    newitemweapon2.setDescription("A grisly looking battle axe")
    newitemweapon2.setDamage(5)
    newitemweapon2.setHands(2)
    game.items_common.append(newitemweapon2)
    
    #####
    newitemarmor = game.OBJECT_CLASSES["Armor"]("cap")
    newitemarmor.addAdjective("leather")
    newitemarmor.setDescription("A cap made out of boiled leather.")
    newitemarmor.setSlotUsed("head")
    game.items_common.append(newitemarmor)
    
    print "Saving items to file..."
    gameinit.saveItems()
    
    #####
    # MOBS
    #####
    
    #####
    game.mobs_common = []
    mob1 = game.OBJECT_CLASSES["Mob"]("Billy")
    mob1.setProper(True)
    mob1.setDescription("A homeless looking dude.")
    game.mobs_common.append(mob1)
    
    # save mob file
    print "Saving mobs to file..."
    gameinit.saveMobs()
        
    #####
    # ZONES
    #####
    
    #####
    newzone = game.ZONE("Billy's Apartment")
    newzone.setDescription("A pretty plain apartment.")
    newzone.zonefile = "apartment.zn"
    
    #####
    bathroom = game.OBJECT_CLASSES["Room"]("Bathroom")
    bathroom.setDescription("You are standing in a bathroom that doesn't look like it has been maintained for some time.  The smells of stale urine fills your nose.  A grungry sink hangs precariously from the tiled wall.")
    bathroom.addDescriptor( {"sink":"The sink hasn't been cleaned in years.  It is layered in soap scum."} )
    bathroom.addExit("north", 1)
    bathroom.addNewItem("sword")
    newzone.addRoom(bathroom)
    
    #####
    livingroom = game.OBJECT_CLASSES["Room"]("Living Room")
    livingroom.setDescription("A pretty boring living room vacant of furniture.  Old posters are pinned lazily to the wall.")
    livingroom.addExit("south", 0)
    livingroom.addNewMob("billy")
    newzone.addRoom(livingroom)
    
    
    game.zones = []
    game.zones.append(newzone)
    
    # save test zones
    print "Saving zones to file..."
    gameinit.saveZones()    
    
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
    newchar.saveToFile("cholo.dat")
    
    #####
    print "\nTest data done."
    
    
