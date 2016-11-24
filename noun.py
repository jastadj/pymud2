
class noun(object):
    def __init__(self, name = "no name"):
        
        self.noundata = { "name":name, "description":"no description", "article":"a"}
        self.noundata.update( {"adjectives":[], "verb":None, "proper":False} )
                
        # calc article
        self.calculatearticle()
    
    # setters
    def setname(self, name):
        self.noundata["name"]= name
        self.calculatearticle()
    
    def setdescription(self, desc):
        self.noundata["description"] = desc
    
    def setarticle(self, article):
        self.noundata["article"] = article
    
    def addadjective(self, adjective):
        self.noundata["adjectives"].append(adjective)
    
    def setverb(self, vstring):
        self.noundata["verb"] = vstring
    
    def setproper(self, proper):
        self.noundata["proper"] = proper
    
    # getters
    def getname(self):
        return self.noundata["name"]
    
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
        return self.noundata["description"]
    
    def getarticle(self):
        return self.noundata["article"]
    
    def getadjectives(self):
        return self.noundata["adjectives"]
    
    def getverb(self):
        return self.noundata["verb"]
    
    def isproper(self):
        return self.noundata["proper"]
    
    # functions
    def calculatearticle(self):
        
        if self.getname() == "":
            self.setarticle("a")
            return
        
        vowels= ['a','e','i','o','u']
        
        self.setarticle("a")
        
        if self.getname()[0] in vowels:
            self.setarticle("an")
    
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
    
