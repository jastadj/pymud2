if __name__ == "__main__":
    
    import defs
    import hubinit
    import hub
    import worldobject
    import account
    import character
    import zone
    import item
    import command
    
    defs.configtestmode()
    #hubinit.hubinittest()
    
    #####
    # USER ACCOUNT
    hub.accounts = account.accountmanager()
    hub.accounts.add("cholo", "cholo")
    print "User accounts = %d" %hub.accounts.count()
    testaccount = hub.accounts.dologin("cholo", "cholo")
    testaccount.data["characterfile"] = "cholo.dat"
    hub.accounts.save()
    
    #####
    # CHARACTERS
    newcharacter = character.character(testaccount)
    newcharacter.save()
    
    
    #####
    # ITEMS

    
    
    
    #####
    # ZONES / ROOMS
    newzone = zone.zone(0, "whiteeagle.zn", True)
    newzone.newroom("White Eagle Tavern")
    newzone.newroom("Hallway")
    newzone.getroom(0).setdescription("The dayroom of this tavern smells of sour booze and stale tobacco.")
    newzone.getroom(1).setdescription("This hallway leads to the various rentable rooms of the tavern.")
    if not newzone.connectrooms( newzone.getroom(0), "east", newzone.getroom(1), "west"):
        print "ERROR CONNECTING ROOMS!"
    
    print ""
    newzone.getroom(0).show()
    
    hub.zones.update( {0:newzone} )
    hubinit.savezones()
    print ""
    newzone.show()
    
    
    
    
    #####
    # WORLD OBJECTS SUMMARY
    
    print ""
    print "uidcount = %d" %worldobject.worldobject.uidcount
    hub.showworldobjects()
    
    #####
    print "\nTest data done."
    
    
    
    hubinit.save()
    
