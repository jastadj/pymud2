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
    myitems.append( item.item("rock") )
    myitems.append( item.item("mug") )
    myitems.append( item.item("dagger") )
    myitems[-1].makeweapon()
    myitems[-1].weapon.setdamage(4)
    
    # store all common items in common items list
    hub.commonitems = myitems

def defaultmobs():
    #####
    # MOBS
    mymobs = []
    mymobs.append( actor.mob("Gil") )
    mymobs[-1].setproper(True)
    mymobs[-1].setattribute("maxhp", 42)
    
    mymobs.append( actor.mob("rabbit") )
    mymobs[-1].setproper(False)
    mymobs[-1].setattribute("maxhp", 3)
    mymobs[-1].addadjective("fluffy")
    # store all common mobs in common mobs list
    hub.commonmobs = mymobs

def defaultzones():
    #####
    # ZONES / ROOMS
    newzone = zone.zone(0, "whiteeagle.zn", True)
    newzone.newroom("White Eagle Tavern")
    newzone.newroom("Hallway")
    newzone.getroom(0).setdescription("The dayroom of this tavern smells of sour booze and stale tobacco. A long polished bar runs along the north side of the room.")
    newzone.getroom(0).adddescriptor({"bar":"The bar looks fairly scuffed up, possibly due to fighting."})
    newzone.getroom(0).newspawner( hub.finduidbyname("dagger"), 5 )
    newzone.getroom(0).newspawner( hub.finduidbyname("gil"), 5 )
    newzone.getroom(1).newspawner( hub.finduidbyname("rabbit"), 5)
    #newzone.getroom(0).additem( hub.commonitems[1].create())
    #newzone.getroom(0).addmob( hub.commonmobs[0].create() )
    newzone.getroom(1).setdescription("This hallway leads to the various rentable rooms of the tavern.")
    newzone.getroom(1).additem( hub.commonitems[2].create())
    newzone.connectrooms( newzone.getroom(0), "east", newzone.getroom(1), "west")

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
    
    
    
    
