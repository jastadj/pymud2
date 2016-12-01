
class noun(object):
    def __init__(self, name = "no name"):
        
        self.noundata = { "name":name, "description":"no description", "article":"a", "plural":None}
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
    
    def setplural(self, plural):
        self.noundata["plural"] = plural
    
    def addadjective(self, adjective):
        self.noundata["adjectives"].append(adjective)
    
    def setverb(self, vstring):
        self.noundata["verb"] = vstring
    
    def setproper(self, proper):
        self.noundata["proper"] = proper
    
    # getters
    def getname(self, quantity = 1):
        if quantity > 1:
            return self.getplural()
        else:
            return self.noundata["name"]
    
    def getnameex(self, quantity = 1, withverb = False):
        dstr = ""
        plural = False
        
        if quantity > 1:
            plural = True
            
            if quantity == 2: dstr += "two "
            elif quantity == 3: dstr += "three "
            elif quantity == 4: dstr += "four "
            elif quantity == 5: dstr += "five "
            elif quantity == 6: dstr += "six "
            elif quantity == 7: dstr += "seven "
            elif quantity == 8: dstr += "eight "
            elif quantity == 9: dstr += "nine "
            elif quantity == 10: dstr += "ten "
            elif quantity > 10: dstr += "many "
        
        # if noun is not proper
        if not self.isproper() and not plural:
            
            # add article
            dstr += "%s " %self.getarticle()
            
        # add adjectives
        for a in self.getadjectives():
            dstr += "%s " %a
        
        # add name
        dstr += self.getname(quantity)
        
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
    
    def getplural(self):
        if self.noundata["plural"] == None:
            return self.noundata["name"] + "s"
        else:
            return self.noundata["plural"]
    
    # functions
    def calculatearticle(self):
        
        if self.getname() == "":
            self.setarticle("a")
            return
        
        vowels= ['a','e','i','o','u']
        
        self.setarticle("a")
        
        if self.getname()[0] in vowels:
            self.setarticle("an")
    
    def hasmatch(self, tstr, quantity = 1):
        
        # empty or return lines are not valid
        if len(tstr) == 0: return False
        
        #split string into words
        tdesc = tstr.split()
        
        # last word should be noun name
        tname = tdesc[-1]
        tdesc.remove(tname)

        # noun name matches at minimum
        if tname.lower() == self.getname(quantity).lower():
            
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
    
    def todict(self):
        tdict = {"noundata":self.noundata}
        
        return tdict
    
    def fromJSON(self, jobj):
        
        self.noundata = jobj["noundata"]
    
if __name__ == "__main__":
    import json
    mynoun = noun("dog")
    mynoun.addadjective("mangy")
    mynoun.setproper(False)
    mynoun.setverb("sitting patiently")
    print mynoun.getnameex() + " " + mynoun.getverb()
    
    
    mynoundict = mynoun.todict()
    mynounjstr = json.dumps(mynoundict)
    mynounjobj = json.loads(mynounjstr)
    mynouncopy = noun()
    mynouncopy.fromJSON(mynounjobj)
    print mynouncopy.getnameex(5) + " " + mynoun.getverb()
