import game

class CommandSet(object):
    
    def __init__(self):
        self.commands = []
        self.aliases = {}
    
    def add(self, name, helpstr, fptr, hasargs = False):
        self.commands.append( Command(name, helpstr, fptr, hasargs) )

    def count(self):        
        return len(self.commands)
    
    def getCommand(self, cstr):
        foundcmds = []
        
        # if command string is an alias
        if cstr in self.aliases.keys():
			cstr = self.aliases[cstr]
        
        for i in range(0, self.count() ):
            #found absolute
            if self.commands[i].cdict["name"] == cstr:
                return [self.commands[i]]
            #found partial match
            elif self.commands[i].cdict["name"].startswith(cstr):
                foundcmds.append(self.commands[i])
        if len(foundcmds) == 0:
            return None
        else:
            return foundcmds
           

class Command(object):
    def __init__(self, name, helpstr, fptr, hasargs = False):
        self.cdict = {"name":name,
                      "helpstring":helpstr,
                      "hasargs":False,
                      "function":fptr}
        if hasargs:
            self.cdict.update({"hasargs":True})
        
        
    def execute(self, tuser, *argv):
        if self.cdict["function"] == None:
            pass
        elif not self.cdict["hasargs"]:
            self.cdict["function"](tuser, self.cdict)
        else:
            args = []
            if len(argv[0]) == 0:
               args.append("")
               args = None
            else:
                for a in argv[0]:
                    args.append(a)
            self.cdict["function"](tuser, self.cdict, args)


def initMainCommands():
    cs = CommandSet()
    cs.add("help", "Show help menu", game.showHelpMenu)
    cs.commands[-1].cdict.update({"source":cs})
    
    cs.add("look", "Look at something", game.doLook, True)
    cs.add("north", "Move north", game.doMove)
    cs.commands[-1].cdict.update({"dir":0})
    cs.add("south", "Move south", game.doMove)
    cs.commands[-1].cdict.update({"dir":1})
    cs.add("east", "Move east", game.doMove)
    cs.commands[-1].cdict.update({"dir":2})
    cs.add("west", "Move west", game.doMove)
    cs.commands[-1].cdict.update({"dir":3})
    
    cs.add("debug", "do something", game.doDebug)
    
    
    # setup command aliases
    cs.aliases.update( {"?":"help"})
    
    return cs

if __name__ == "__main__":
    import testuser
    
    tuser = testuser.TestUser()
    
    doquit = False
    
    def t(tuser, cdict):
        tuser.send("This is a test function!\n")
    
    def ta(tuser, cdict, *argv):
        tuser.send("This is a test function with args!\n")
        if argv[0] == None:
            print "No args"
        else:
            for a in argv[0]:
                print a
    
    def quittest(tuser, cdict):
        global doquit
        doquit = True
    
    def dohelp(tuser, cdict):
        print "Help Menu"
        print "---------"
        for i in cset.commands:
            print "%s - %s" %(i.cdict["name"], i.cdict["helpstring"])
    
    cset = CommandSet()
    cset.add("t", "Tests a function with no args", t)
    cset.add("ta", "Tests a function with args", ta, True)
    cset.add("help", "Help menu", dohelp)
    cset.add("quit", "Quit test", quittest)
    
    cset.aliases.update( {"?":"help"} )
    
    while not doquit:
        
        tuser.send(">")
        tuser.last_input = raw_input()
        
        cmds = tuser.last_input.split()
        
        
        # if no commands were entered, ignore
        if len(cmds) == 0:
            continue
         
        # get commands from input
        tcmd = cset.getCommand(cmds[0])
        
        # if no valid command was found
        if tcmd == None:
            tuser.send("Invalid command!\n")
        # if only one command was found, execute
        elif len(tcmd) == 1:
            tcmd[0].execute(tuser,cmds[1:])
        # or if multiple commands found, print them
        else:
            for c in tcmd:
                print a.cdict["name"]
        
        
        
