
INITIAL_DOMAIN=[1-9]

class Cell:
    def __init__(self,_i,_j,_value=0):
        self.value =_value
        self.i=_i
        self.j=_j
        if _value==0:
            self.isEmpty=False
        else:
            self.isEmpty=True

class EmptyCell(Cell):
    def __init__(self):
        super().__init__()
        self.domain=INITIAL_DOMAIN
    
    def removeDomain(self,_n):
        try:
            self.domain.remove(_n)
        except:
            pass
            
    