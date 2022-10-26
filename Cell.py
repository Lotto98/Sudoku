
INITIAL_DOMAIN=range(1,10)

class Cell:
    def __init__(self,_i,_j,_value=0):
        self.value =int(_value)
        self.i=_i
        self.j=_j
        if _value==0:
            self.isEmpty=False
        else:
            self.isEmpty=True
    def __str__(self) -> str:
       return str(self.value)
    def __repr__(self):
        return str(self)

class EmptyCell(Cell):
    def __init__(self):
        super().__init__()
        self.domain=INITIAL_DOMAIN
    
    def removeDomain(self,_n):
        try:
            self.domain.remove(_n)
        except:
            pass

class FullCell(Cell):
    def __init__(self, _i, _j, _value):
        super().__init__(_i, _j, _value)
            
    