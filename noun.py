
class Noun(object):
    def __init__(self, name = "no name"):
        self.name = name
        self.description = "No description."
        self.article = "a"
        self.adjectives = []
        self.verb = None        
        self.proper = False
        
        
        # calc article
        self.calculateArticle()
    
    # setters
    def setName(self, name):
        self.name = name
        self.calculateArticle()
    
    def setDescription(self, desc):
        self.description = desc
    
    def setArticle(self, article):
        self.article = article
    
    def addAdjective(self, adjective):
        self.adjectives.append(adjective)
    
    def setVerb(self, vstring):
        self.verb = vstring
    
    def setProper(self, proper):
        self.proper = proper
    
    # getters
    def getName(self):
        return self.name
    
    def getExName(self, withverb = False):
        dstr = ""
        
        # if noun is not proper
        if not self.isProper():
            
            # add article
            dstr += "%s " %self.getArticle()
            
            # add adjectives
            for a in self.getAdjectives():
                dstr += "%s " %a
        
        # add name
        dstr += self.getName()
        
        # apply verb string
        if withverb:
            if self.getVerb() != None:
                dstr += " %s" %self.getVerb()
        
        # return resultant extended name
        return dstr
    
    def getDescription(self):
        return self.description
    
    def getArticle(self):
        return self.article
    
    def getAdjectives(self):
        return self.adjectives
    
    def getVerb(self):
        return self.verb
    
    def isProper(self):
        return self.proper
    
    # functions
    def calculateArticle(self):
        
        vowels= ['a','e','i','o','u']
        
        self.article = "a"
        
        if self.name[0] in vowels:
            self.article = "an"
    
    def hasMatch(self, tstr):
        
        # empty or return lines are not valid
        if len(tstr) == 0: return False
        
        #split string into words
        tdesc = tstr.split()
        
        # last word should be noun name
        tname = tdesc[-1]
        tdesc.remove(tname)
        
        # noun name matches at minimum
        if tname.lower() == self.getName().lower():
            
            validwords = []
            
            if not self.isProper():
                # get valid words
                validwords += self.getAdjectives()
                # add article to the list
                validwords += self.getArticle()
                
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
        
    def saveToStrings(self):
    
        tstrings = []
        
        ttype = self.__class__.__name__
        
        tstrings.append("%s_name:%s" %(ttype, self.getName() ) )
        tstrings.append("%s_description:%s" %(ttype, self.getDescription() ) )
        tstrings.append("%s_proper:%s" %(ttype, self.isProper() ) )
        tstrings.append("%s_verb:%s" %(ttype, self.getVerb() ) )
        
        # if noun is not proper
        if not self.isProper():
            
            tstrings.append("%s_article:%s" %(ttype, self.article) )
            
            # get adjectives
            for a in self.getAdjectives():
                tstrings.append("%s_adjective:%s" %(ttype, a) )
        
        return tstrings
        
    def loadFromStrings(self, tstrings):
        
        ttype = self.__class__.__name__
        
        for line in tstrings:
            
            dfind = line.find(':')
            
            key = line[:dfind]
            val = line[dfind+1:]

            if key == "%s_name" %ttype:
                self.setName(val)
            
            elif key == "%s_description" %ttype:
                self.setDescription(val)
            
            elif key == "%s_proper" %ttype:
                if val == "False":
                    val = False
                else: val = True
                
                self.setProper(val)
            
            elif key == "%s_verb" %ttype:
                if val == "None":
                    val = None
                self.setVerb(val)
            
            elif key == "%s_article" %ttype:
                self.setArticle(val)
                
            elif key == "%s_adjective" %ttype:
                self.addAdjective(val)



    
    
if __name__ == "__main__":
    
    # create a noun
    noun1 = Noun("pencil")
    noun1.setProper(False)
    noun1.addAdjective("sturdy")
    noun1.setVerb("spinning on the table")
    
    print "Noun1:"
    print noun1.getExName()
    
    # save noun to strings
    print "\nSave to strings:"
    n1strings = noun1.saveToStrings()
    for line in n1strings:
        print line
    
    # load another noun with strings from first noun
    print "\nLoad Noun2 with Noun1 strings:"
    noun2 = Noun()
    noun2.loadFromStrings(n1strings)
    print noun2.getExName()
    
    doquit = False
    
    # test various string matches with noun
    print "\nCheck words against Noun2:"
    while not doquit:
        
        print "\nNoun String:%s" %noun2.getExName()
        userin = raw_input(">")
        
        print "input:%s" %userin
        
        if userin == "quit": doquit = True
        else:
            print noun2.hasMatch(userin)