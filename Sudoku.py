from queue import LifoQueue
from Cell import Cell, INITIAL_DOMAIN
from tabulate import tabulate

class Sudoku:
    def __init__(self,filename: str):
        """
        Sudoku constructor.
        
        Args:
            filename (str): sudoku file.
        """
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
        """
        Function that prints sudoku as a matrix of a better visualization.
        """
        print(tabulate(self.sudoku,headers="keys",showindex=True,tablefmt="outline"))
        
        if len(self.sudoku)!=9:
            print("Warning: malformed sudoku, number of rows is not 9")
            
        for n,row in enumerate(self.sudoku):
            if len(row)!=9:
                print("Warning: malformed sudoku in row "+str(n))


    def __checkDigits(self,l: list[Cell]):
        """
        Functions that given a list of cells checks if all the 9 digits are present.

        Args:
            l (list[Cell]): list of cells.

        Returns:
            bool: 'True' if there are all and only the 9 sudoku digits.
        """
        
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
        """
        Function that returns the cells of the sudoku square at indexes 'i' and 'j' as a list.
        
        Args:
            i (int): row index. 
            j (int): col index.

        Returns:
            list[Cell]: list of cells in the square.
        """
        l=[]
        for r in range(i,i+3):
            for c in range(j,j+3):
                l.append(self.sudoku[r][c])
        return l            
        
    def checkSudoku(self):
        """
        Function that checks the sudoku correctness.

        Returns:
            bool: 'True' if the sudoku is correct, 'False' othewise.
        """
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
        """
        Function that return the sudoku cell with minimum domain.
        
        Returns:
            Cell: min domain cell.
        """
        return min([item for sublist in self.sudoku for item in sublist], key=lambda x: x.getDomainLen())
    
    def __whichSquare(self,n:int):
        """
        Given an sudoku index return the index of the associated square.
        
        Args:
            n (int): sudoku index.

        Returns:
            int: square index.
        """
        if n<3:
            return 0
        if n<6:
            return 3
        if n<9:
            return 6
    
    def __removeDomainRow(self,index:int, value:int)->set[Cell]:
        """
        Function that removes from row of index 'index' the specific 'value'.

        Args:
            index (int): row index.
            value (int): value to be removed.

        Returns:
            set[Cell]: cells in which value was removed from their domain.
        """
        domainRemovedCells=set()
        for cell in self.sudoku[index]:
            if cell.removeDomain(value):
                domainRemovedCells.add(cell)
        return domainRemovedCells    
        
    def __removeDomainCol(self,index:int, value:int)->set[Cell]:
        """
        Function that removes from col of index 'index' the specific 'value'.

        Args:
            index (int): col index.
            value (int): value to be removed.

        Returns:
            set[Cell]: cells in which value was removed from their domain.
        """
        domainRemovedCells=set()
        for cell in list(zip(*self.sudoku))[index]:
            if cell.removeDomain(value):
                domainRemovedCells.add(cell)
        return domainRemovedCells
        
    def __removeDomainSquare(self,indexR:int,indexC:int,value:int)->set[Cell]:
        """
        Function that removes from square of indexes 'indexR' and 'indexC' the specific 'value'.

        Args:
            indexR (int): row index.
            indexC (int): col index.
            value (int): value to be removed.

        Returns:
            set[Cell]: cells in which value was removed from their domain.
        """
        domainRemovedCells=set()
        for cell in self.__square( self.__whichSquare(indexR), self.__whichSquare(indexC) ):
            if cell.removeDomain(value):
                domainRemovedCells.add(cell)
        return domainRemovedCells
            
    def __removeDomainAll(self,r:int,c:int,value:int)->set[Cell]:
        """
        Function that removes from row of index 'r', col of index 'c' and square of indexes 'r' and 'c' the specific 'value'.

        Args:
            r (int): row index.
            c (int): col index.
            value (int): value to be removed.

        Returns:
            set[Cell]: cells in which value was removed from their domain.
        """
        return self.__removeDomainRow(r,value) | self.__removeDomainCol(c,value) | self.__removeDomainSquare(r,c,value)
    
    def __CP(self):
        """
        CP in sudoku. It updates the domain of the empty cells present in row, col or square of every full cell.
        """
        for r in range(0,9):      
            for c in range(0,9):            
                if not self.sudoku[r][c].isEmpty:
                    self.__removeDomainAll(r,c,self.sudoku[r][c].value)        
    
            
    def sudokuSolverCP(self):
        
        """
        Sudoku solver with CP and backtracking approch.
        """
        
        #Queue of visited cells
        visited_cells=LifoQueue()
        
        #initial constraint propagation
        self.__CP()
        
        #retrive the min cell domain
        min_cell=self.__minDomain()
        
        #if the min domain cell is a full cell then the computation is over
        while min_cell.isEmpty:
            
            #if there is at least one value that was not previusly assigned in the min domain cell domain then:
            if len(min_cell.domain-min_cell.visitedDomain)>0:
                
                #1) update value of the min domain cell
                min_cell.value=(min_cell.domain-min_cell.visitedDomain).pop()
                min_cell.visitedDomain.add(min_cell.value)
                
                #2) update min domain cell to a full cell
                min_cell.isEmpty=False
            
                #3) update domains of row, col and square by removing the value assigned to the min domain cell
                domainRemovedCells=self.__removeDomainAll(min_cell.i,min_cell.j,min_cell.value)
            
                #4) add the min cell and the cells in which the domain is modified to the visited cells queue as a tuple
                visited_cells.put((min_cell,domainRemovedCells))
            
                #5) retrive the next min domain cell
                min_cell=self.__minDomain()
            
            #if the cell domain is empty or if all the values in the cell domain were previusly assigned backtracking:   
            else:
                
                #1) reset visited domain for min domain cell
                min_cell.visitedDomain=set()
                
                #2) get last visited cell and the cell in which the domain was modified by its assignement
                last_visited_cell,domainRemovedCells=visited_cells.get()
                
                #3) update last visited cell to a empty cell
                last_visited_cell.isEmpty=True
                
                #4) add the value previusly assigned to the last visited cell to the cells previusly modified by its assignment
                for cell in domainRemovedCells:
                    cell.addDomain(last_visited_cell.value)
                
                #5) set the min domain cell as the last visited cell to explore the next value of its domain
                min_cell=last_visited_cell