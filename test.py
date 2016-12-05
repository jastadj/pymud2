import defs
import hubinit
import hub
import worldobject
import account
import character
import zone
import item
import actor
import command


def defaultaccounts():
    #####
    # USER ACCOUNT
    hub.accounts = account.accountmanager()
    hub.accounts.add("cholo", "cholo")
    print "User accounts = %d" %hub.accounts.count()
    testaccount = hub.accounts.dologin("cholo", "cholo")
    testaccount.data["characterfile"] = "cholo.dat"
    
    
    hub.accounts.add("j","j")
    testaccount2 = hub.accounts.dologin("j","j")
    testaccount2.data["characterfile"] = "john.dat"
    
    hub.accounts.save()
    
    #####
    # CHARACTERS
    newcharacter = character.character(testaccount, "Cholo")
    newcharacter.setattribute("maxhp", 12)
    newcharacter.setattribute("hp", 12)
    newcharacter.save()

    newchar2 = character.character(testaccount2, "John")
    newchar2.setattribute("maxhp", 12)
    newchar2.setattribute("hp", 12)
    newchar2.save()

def defaultitems():
    #####
    # ITEMS
    myitems = []
    
    myitems.append( item.item("corpse") )
    myitems[-1].makecorpse()
    
    myitems.append( item.item("coin") )
    myitems[-1].addadjective("gold")
    myitems[-1].setdescription("Gold currency.")
    myitems[-1].setstackable(True)
    
    myitems.append( item.item("sign") )
    myitems[-1].addadjective("white")
    myitems[-1].addadjective("eagle")
    myitems[-1].makesign()
    myitems[-1].sign.settext("  #c3WELCOME TO THE WHITE EAGLE#cr\n")
    myitems[-1].setstatic(True)
    myitems[-1].setunlisted(True)
    
    myitems.append( item.item("rock") )
    myitems[-1].setdescription("Just a dirty old rock.")    
    
    myitems.append( item.item("mug") )
    myitems[-1].setdescription("A small ceramic mug.")    
    
    myitems.append( item.item("dagger") )
    myitems[-1].makeweapon()
    myitems[-1].weapon.setdamage(4)
    myitems[-1].setdescription("A small but lethal dagger.")
    
    myitems.append( item.item("sack") )
    myitems[-1].setdescription("A small leather sack used for storing things.")
    myitems[-1].addadjective("small")
    myitems[-1].addadjective("leather")
    myitems[-1].makecontainer()
    
    myitems.append( item.item("bread"))
    myitems[-1].setdescription("A piece of crusty bread.")
    myitems[-1].addadjective("piece of")
    myitems[-1].makefood()
    
    myitems.append( item.item("beer"))
    myitems[-1].setdescription("A mug of beer.")
    myitems[-1].makedrink()
    
    myitems.append( item.item("jacket") )
    myitems[-1].setdescription("A well oiled dark leather jacket.")
    myitems[-1].addadjective("leather")
    myitems[-1].makearmor()
    myitems[-1].armor.addbodypart( defs.BODYPART_LEFTARM)
    myitems[-1].armor.addbodypart( defs.BODYPART_RIGHTARM)
    myitems[-1].armor.addbodypart( defs.BODYPART_TORSO)
    
    
    # store all common items in common items list
    hub.commonitems = myitems

def defaultmobs():
    #####
    # MOBS
    mymobs = []
    mymobs.append( actor.mob("Gil") )
    mymobs[-1].setdescription("He looks like a no-nonsense bartender.")
    mymobs[-1].setproper(True)
    mymobs[-1].setattribute("maxhp", 42)
    
    mymobs.append( actor.mob("rabbit") )
    mymobs[-1].setdescription("A cute little bunny rabbit.")
    mymobs[-1].setproper(False)
    mymobs[-1].setattribute("maxhp", 3)
    mymobs[-1].addadjective("fluffy")
    # store all common mobs in common mobs list
    hub.commonmobs = mymobs

def defaultzones():
    #####
    # ZONES / ROOMS
    newzone = zone.zone(0, "whiteeagle.zn", True)
    newzone.newroom("White Eagle Tavern") #0
    newzone.newroom("Hallway") #1
    newzone.newroom("Store Room") #2
    newzone.newroom("Cellar") #3
    newzone.newroom("Tatton Road") #4
    newzone.newroom("Tatton Road") #5
    newzone.newroom("Tatton Road") #6
    newzone.newroom("Armorer") #7
    newzone.getroom(0).setdescription("You are standing in a narrow tavern that runs east to west. It smells of sour booze and stale tobacco. A long polished bar runs along the north side of the room. Various crusty regulars sit huddled together in clumps.")
    newzone.getroom(0).adddescriptor({"bar":"The bar looks fairly scuffed up, possibly due to fighting."})
    newzone.getroom(0).newspawner( hub.finduidbyname("white eagle sign"), 5000)
    newzone.getroom(0).newspawner( hub.finduidbyname("dagger"), 5 )
    newzone.getroom(0).getspawners()[-1].setmaxcount(1)
    newzone.getroom(0).newspawner( hub.finduidbyname("gil"), 5 )
    newzone.getroom(1).newspawner( hub.finduidbyname("rabbit"), 5)
    newzone.getroom(1).newspawner( hub.finduidbyname("sack"), 5000)
    newzone.getroom(1).setdescription("This hallway leads to the various rentable rooms of the tavern.")
    newzone.getroom(1).additem( hub.commonitems[2].create())
    newzone.getroom(2).setdescription("This is the storeroom of the White Eagle.  Various shelves and crates fill the room.  It smells slightly musty here but looks pretty well maintained.")
    newzone.getroom(2).adddescriptor({"shelves":"The shelves are lined with various jars."})
    newzone.getroom(2).adddescriptor({"jars":"The jars on the shelves contain various pickled or preserved foods."})
    newzone.getroom(2).adddescriptor({"crates":"Several large crates take up most of the space in the storeroom."})
    newzone.getroom(2).newspawner( hub.finduidbyname("bread"), 5)
    newzone.getroom(2).newspawner( hub.finduidbyname("beer"), 5)
    newzone.getroom(3).setdescription("A dusty old cellar.")
    newzone.getroom(3).newspawner( hub.finduidbyname("coin"), 5)
    newzone.getroom(3).getspawners()[-1].setstack(5)
    newzone.getroom(4).setdescription("Tatton road stretches from east to west.")
    newzone.getroom(5).setdescription("Tatton road stretches from east to west.")
    newzone.getroom(6).setdescription("Tatton road stretches from east to west.")
    newzone.getroom(7).setdescription("You are standing in the armorer's shop.  It smells of leather and oil.")
    newzone.getroom(7).newspawner( hub.finduidbyname("leather jacket"), 5)
    newzone.connectrooms( newzone.getroom(0), "east", newzone.getroom(1), "west")
    newzone.connectrooms( newzone.getroom(0), "west", newzone.getroom(2), "east")
    newzone.connectrooms( newzone.getroom(0), "down", newzone.getroom(3), "up")
    newzone.connectrooms( newzone.getroom(0), "south", newzone.getroom(4), "north")
    newzone.connectrooms( newzone.getroom(4), "west", newzone.getroom(5), "east")
    newzone.connectrooms( newzone.getroom(4), "east", newzone.getroom(6), "west")
    newzone.connectrooms( newzone.getroom(4), "south", newzone.getroom(7), "north")

    hub.zones.update( {0:newzone} )

    #hubinit.savezones()

if __name__ == "__main__":
    
    deletetestfolder = True
    
    if deletetestfolder:
        import shutil
        try:
            shutil.rmtree('./test')
            print "Removed test folder."     
        except:
            print "Could not remove test folder."
            pass
    
    defs.configtestmode()
    #hubinit.hubinittest()
    
    defaultaccounts()

    defaultitems()
    
    defaultmobs()

    defaultzones()    

    print ""
    print "uidcount = %d" %worldobject.worldobject.uidcount
    hub.showworldobjects()
    
    #####
    print "\nTest data done."
    hubinit.save()
    
    
    
    
