
class noun(object):
    def __init__(self, name = "no name"):
        self.name = name
        self.description = "No description."
        self.article = "a"
        self.adjectives = []
        self.verb = None        
        self.proper = False
        
        
        # calc article
        self.calculatearticle()
    
    # setters
    def setname(self, name):
        self.name = name
        self.calculatearticle()
    
    def setdescription(self, desc):
        self.description = desc
    
    def setarticle(self, article):
        self.article = article
    
    def addadjective(self, adjective):
        self.adjectives.append(adjective)
    
    def setverb(self, vstring):
        self.verb = vstring
    
    def setproper(self, proper):
        self.proper = proper
    
    # getters
    def getname(self):
        return self.name
    
    def getnameex(self, withverb = False):
        dstr = ""
        
        # if noun is not proper
        if not self.isproper():
            
            # add article
            dstr += "%s " %self.getarticle()
            
            # add adjectives
            for a in self.getadjectives():
                dstr += "%s " %a
        
        # add name
        dstr += self.getname()
        
        # apply verb string
        if withverb:
            if self.getverb() != None:
                dstr += " %s" %self.getverb()
        
        # return resultant extended name
        return dstr
    
    def getdescription(self):
        return self.description
    
    def getarticle(self):
        return self.article
    
    def getadjectives(self):
        return self.adjectives
    
    def getverb(self):
        return self.verb
    
    def isproper(self):
        return self.proper
    
    # functions
    def calculatearticle(self):
        
        if self.name == "":
            self.article = "a"
            return
        
        vowels= ['a','e','i','o','u']
        
        self.article = "a"
        
        if self.name[0] in vowels:
            self.article = "an"
    
    def hasmatch(self, tstr):
        
        # empty or return lines are not valid
        if len(tstr) == 0: return False
        
        #split string into words
        tdesc = tstr.split()
        
        # last word should be noun name
        tname = tdesc[-1]
        tdesc.remove(tname)
        
        # noun name matches at minimum
        if tname.lower() == self.getname().lower():
            
            validwords = []
            
            if not self.isproper():
                # get valid words
                validwords += self.getadjectives()
                # add article to the list
                validwords += self.getarticle()
                
                # lower all valid words
                for vw in validwords:
                    vw = vw.lower()
                
            # check if any of the other words match
            for a in tdesc:
                if a.lower() not in validwords:
                    return False

        # noun name does not match
        else: return False
        
        # matching passes
        return True
    
    
if __name__ == "__main__":
    mynoun = noun("dog")
    mynoun.addadjective("mangy")
    mynoun.setproper(False)
    mynoun.setverb("sitting patiently")
    
    print mynoun.getnameex() + " " + mynoun.getverb()
    
