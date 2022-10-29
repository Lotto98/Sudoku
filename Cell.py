
INITIAL_DOMAIN=set([x for x in range(1,10)])

class Cell:
    
    def __init__(self,_i,_j,_value=0):
        
        self.value =int(_value)
        self.i=_i
        self.j=_j
        
        if _value!=0:
            self.isEmpty=False
        else:
            self.isEmpty=True
            self.domain=set(INITIAL_DOMAIN)
            
    def __str__(self):
        if self.isEmpty:        
            return str(self.value)+str(self.domain)
        else:
            return str(self.value)
        
    def __repr__(self):
        return str(self)
    
    def printDomain(self):
        if self.isEmpty:
            print(self.domain)
        else:
            pass
    
    def getDomainLen(self):
        if self.isEmpty:
            return len(self.domain)
        else:
            return 10
        
    def getCordinates(self):
        return(self.i,self.j)
    
    def removeDomain(self,_n):
        if self.isEmpty:
            try:
                self.domain.remove(_n)
            except:
                    pass
    
    def addDomain(self,_n):
        if self.isEmpty:
            self.domain.add(_n)
            
    