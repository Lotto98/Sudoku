from __future__ import annotations

INITIAL_DOMAIN=set([x for x in range(1,10)])

class Cell:
    
    def __init__(self,_i:int,_j:int,_value:int=0):
        """
        sudoku cell constructor. All cells have row and col indexes (ints), value (int) and isEmpty (bool).
        Empty cells have in addition 'domain' and 'visitedDomain'.

        Args:
            _i (int): row index of the cell.
            _j (int): col index of the cell.
            _value (int, optional): value of the cell. Defaults to 0 for empty cells.
        """
        
        self.value =int(_value)
        self.i=_i
        self.j=_j
        
        if self.value!=0:
            self.isEmpty=False
        else:
            self.isEmpty=True
            self.domain=set(INITIAL_DOMAIN)
            self.visitedDomain=set()
            
    def __str__(self):
        """
        toString function.
        
        Returns:
            str: cell string.
        """
        if self.isEmpty:        
            return str(self.value) #"-"
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
        
    def getCoordinates(self):
        return(self.i,self.j)
    
    def removeDomain(self,_n:int):
        """
            Function that removes a specific value from the cell domain.
        Args:
            _n (int): _description_

        Returns:
            bool: 'True' if the _n is removed correctly, 'False' otherwise.
        """
        if self.isEmpty:
            try:
                self.domain.remove(_n)
                return True
            except:
                return False
    
    def addDomain(self,_n:int):
        if self.isEmpty:
            self.domain.add(_n)
            return True
        else:
            return False
            
    #def __eq__(self, __o: Cell) -> bool:
        #return self.value==__o.value
        
            
    