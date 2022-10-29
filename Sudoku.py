from queue import LifoQueue
from Cell import *
from tabulate import tabulate

class Sudoku:
    def __init__(self,filename: str):
        self.sudoku=[]
        with open(filename) as file:
            for i,line in enumerate(file):
                line=line.strip('\n')
                row=[]
                self.sudoku.append(row)
                for j,x in enumerate(line):
                    if int(x)==0:
                        row.append(Cell(i,j))
                    else:
                        row.append(Cell(i,j,_value=int(x)))
        
    def printSudoku(self):
        print(tabulate(self.sudoku,headers="keys",showindex=True,tablefmt="outline"))
        
        if len(self.sudoku)!=9:
            print("Warning: malformed sudoku, number of rows is not 9")
            
        for n,row in enumerate(self.sudoku):
            if len(row)!=9:
                print("Warning: malformed sudoku in row "+str(n))


    def __checkDigits(self,l: list[Cell]):
        
        domain=list(INITIAL_DOMAIN)
        
        if len(l)!=9:
            print("malformed sudoku",end='')
            return False
        
        for e in l:
            x=e.value
            if x>9 or x<1:
                print("outside domain boundaries",end='')
                return False
            
            try:
                domain.remove(x)
            except:
                print("multiple occorences of same number ("+str(x)+")",end='')
                return False;
        
        if len(domain)!=0:
            print("digits: "+str(domain)+" not present",end='')
            return False
        return True

    def __square(self, i:int, j:int)->list[Cell]:
        l=[]
        for r in range(i,i+3):
            for c in range(j,j+3):
                l.append(self.sudoku[r][c])
        return l            
        
    def checkSudoku(self):
        #check rows
        for n,row in enumerate(self.sudoku):
            if not self.__checkDigits(row):
                print(" in row "+str(n))
                return False
        #check cols
        for n,col in enumerate(list(zip(*self.sudoku))[1:]):
            if not self.__checkDigits(col):
                print(" in col "+str(n))
                return False
        #check squares
        for row_start in range(0,8,3):
            for col_start in range(0,8,3):
                if not self.__checkDigits(self.__square(row_start,col_start)):
                    print(" in square: "+str(row_start)+","+str(col_start))
                    return False
        return True
    
    def __minDomain(self)->Cell:
        return min([item for sublist in self.sudoku for item in sublist], key=lambda x: x.getDomainLen())
    
    def __whichSquare(self,n):
        if n<3:
            return 0
        if n<6:
            return 3
        if n<9:
            return 6
    
    def __removeDomainRow(self,index, value):
        for cell in self.sudoku[index]:
            cell.removeDomain(value)
        
    def __removeDomainCol(self,index, value):
        for cell in list(zip(*self.sudoku))[index]:
            cell.removeDomain(value)
        
    def __removeDomainSquare(self,indexR,indexC,value):
        for cell in self.__square( self.__whichSquare(indexR), self.__whichSquare(indexC) ):
            cell.removeDomain(value)
            
    def __removeDomainAll(self,r,c,value):
        self.__removeDomainRow(r,value)
        self.__removeDomainCol(c,value)
        self.__removeDomainSquare(r,c,value)
            
    def __addDomainRow(self,index, value):
        for cell in self.sudoku[index]:
            cell.addDomain(value)
        
    def __addDomainCol(self,index, value):
        for cell in list(zip(*self.sudoku))[index]:
            cell.addDomain(value)
        
    def __addDomainSquare(self,indexR,indexC,value):
        for cell in self.__square(self.__whichSquare(indexR),self.__whichSquare(indexC)):
            cell.addDomain(value)
            
    def __addDomainAll(self,r,c,value):
        self.__addDomainRow(r,value)
        self.__addDomainCol(c,value)
        self.__addDomainSquare(r,c,value)
    
    def CP(self, value=None):
        for r in range(0,9):      
            for c in range(0,9):            
                if not self.sudoku[r][c].isEmpty and (self.sudoku[r][c].value==value or (value is None)):
                    self.__removeDomainAll(r,c,self.sudoku[r][c].value)
    
    def __solverRec(self, min_cell,visited_cells):
        
        if not min_cell.isEmpty:
            return;    
        try:
            self.printSudoku()
            print(min_cell.getCordinates())
            #update value
            min_cell.value=min_cell.domain.pop()    
        except:
            #if the domain set is empty
            
            #get last visited cell
            last_visited_cell=visited_cells.get()
            
            #cell is Empty now
            last_visited_cell.isEmpty=True
            
            #update domains of row, col and square
            self.__addDomainAll(last_visited_cell.i,last_visited_cell.j,last_visited_cell.value)
            self.CP(last_visited_cell.value)
            
            #remove value from domain
            last_visited_cell.removeDomain(last_visited_cell.value)
            
            #loop
            self.__solverRec(last_visited_cell,visited_cells)
        else:
            #cell no longer empty
            min_cell.isEmpty=False
            
            #update domains of row, col and square
            self.__removeDomainAll(min_cell.i,min_cell.j,min_cell.value)
            
            #visited
            visited_cells.put((min_cell))
        
            #loop
            self.__solverRec(self.__minDomain(),visited_cells)
            
    def sudokuSolver(self):
        self.CP()
        min_cell=self.__minDomain()
        visited_cells=LifoQueue()
        self.__solverRec(min_cell,visited_cells)