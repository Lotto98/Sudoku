from __future__ import annotations
import gc
import operator
import time
from Cell import Cell,INITIAL_DOMAIN

import numpy as np

import copy

from queue import LifoQueue

from random import randint,choice,sample,shuffle

from tabulate import tabulate

class Sudoku:
    def __init__(self,_sudoku=None):
        """
        Create a sudoku object from a file or from another sudoku object.

        Args:
            _sudoku (str or Sudoku): .
        """
        if _sudoku is None:
            self.board=[[] for x in range(9)]
        elif isinstance(_sudoku,str):
            self.board=[]
            with open(_sudoku) as file:
                for i,line in enumerate(file):
                    line=line.strip('\n')
                    row=[]
                    self.board.append(row)
                    for j,x in enumerate(line):
                        if int(x)==0:
                            row.append(Cell(i,j))
                        else:
                            row.append(Cell(i,j,_value=int(x)))
            self.finished=False
        elif isinstance(_sudoku,Sudoku):
            self.board=copy.deepcopy(_sudoku.board)
            self.finished=False
        else:
            raise TypeError("Expected a str or sudoku object, found "+str(type(_sudoku)))
    
    def __str__(self):
        """
        Function that prints sudoku as a matrix of a better visualization.
        """
        print()
        
        if len(self.board)!=9:
            print("Warning: malformed sudoku, number of rows is not 9")
            
        for n,row in enumerate(self.board):
            if len(row)!=9:
                print("Warning: malformed sudoku in row "+str(n))
        
        return tabulate(self.board ,headers="keys",showindex=True,tablefmt="outline")

    @staticmethod 
    def __checkDigits(l: list[Cell]):
        """
        Functions that given a list of cells checks if all the 9 digits are present.

        Args:
            l (list[Cell]): list of cells.

        Returns:
            bool: 'True' if there are all and only the 9 sudoku digits.
        """
        
        domain=list(INITIAL_DOMAIN)
        
        #print(l)
        
        if len(l)!=9:
            
            print("malformed sudoku",end='')
            return False
        
        for e in l:
            x=e.value
            if x>9 or x<1:
                
                print("outside domain boundaries",end='')
                if x==0:
                    print(" (sudoku is incomplete)",end='')
                return False
            
            try:
                domain.remove(x)
            except:
                
                print("multiple occurrences of same number ("+str(x)+")",end='')
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
                l.append(self.board[r][c])
        return l            
        
    def checkSudoku(self):
        """
        Function that checks the sudoku correctness.

        Returns:
            bool: 'True' if the sudoku is correct, 'False' otherwise.
        """
        #check rows
        for n,row in enumerate(self.board):
            if not self.__checkDigits(row):
                print(" in row "+str(n))
                return False
        #check cols
        for n,col in enumerate(list(zip(*self.board))):
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
    
    def toNumpy(self):
        
        sudoku_values=[]
        mask=[]
        
        for row in self.board:
            for cell in row:
                sudoku_values.append(cell.value)
                if cell.isEmpty:
                    mask.append(True)
                else:
                    mask.append(False)
        
        return np.array(sudoku_values,dtype=int).reshape(9,9),np.array(mask,dtype=int).reshape(9,9)
    
    def toFile(self,file:str):
        board=self.board
        with open(file, "w") as f:
            for row in board:
                f.writelines([str(number) for number in Sudoku.__toNumbersSet(row)]+["\n"])
                
    def countFullCells(self)->int:
        count=0
        for row in self.board:
            for cell in row:
                if not cell.isEmpty:
                    count+=1
        return count
    
    """
    Constraint propagation & Backtracking Approach
    """
    
    def __minDomain(self)->Cell:
        """
        Function that return the sudoku cell with minimum domain.
        
        Returns:
            Cell: min domain cell.
        """
        return min([item for sublist in self.board for item in sublist], key=lambda x: x.getDomainLen())
    
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
    
    def __removeDomainRow(self, index:int, value:int)->set[Cell]:
        """
        Function that removes from row of index 'index' the specific 'value'.

        Args:
            index (int): row index.
            value (int): value to be removed.

        Returns:
            set[Cell]: cells in which value was removed from their domain.
        """
        domainRemovedCells=set()
        for cell in self.board[index]:
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
        for cell in list(zip(*self.board))[index]:
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
        CP in sudoku. It updates the domains of the empty cells present in row, col or square of every full cell.
        """
        for r in range(0,9):      
            for c in range(0,9):            
                if not self.board[r][c].isEmpty:
                    self.__removeDomainAll(r,c,self.board[r][c].value)        
    
            
    def sudokuSolverCP(self):
        
        """
        Sudoku solver with CP and backtracking approach.
        """
        
        backtracked_nodes=0
        
        #Queue of visited cells
        visited_cells=LifoQueue()
        
        #initial constraint propagation
        self.__CP()
        
        #retrieve the min cell domain
        min_cell=self.__minDomain()
        
        #if the min domain cell is a full cell then the computation is over
        while min_cell.isEmpty:
            
            #if there is at least one value that was not previously assigned in the min domain cell domain then:
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
            
                #5) retrieve the next min domain cell
                min_cell=self.__minDomain()
            
            #if the cell domain is empty or if all the values in the cell domain were previously assigned backtracking:   
            else:
                
                backtracked_nodes+=1
                
                #1) reset visited domain for min domain cell
                min_cell.visitedDomain=set()
                
                #2) get last visited cell and the cells in which the domain was modified by its assignment
                last_visited_cell,domainRemovedCells=visited_cells.get()
                
                #3) update last visited cell to a empty cell
                last_visited_cell.isEmpty=True
                
                #4) add the value previously assigned to the last visited cell to the cells previously modified by its assignment
                for cell in domainRemovedCells:
                    cell.addDomain(last_visited_cell.value)
                
                #5) set the min domain cell as the last visited cell to explore the next value of its domain
                min_cell=last_visited_cell
        
        return backtracked_nodes
                
    """
    Genetic Algorithm approach
    """
    
    @staticmethod
    def __toNumbersSet(l:list[Cell])->list[int]:
        
        return set([cell.value for cell in l])
    
    def __fitness(self):
        
        satisfied_constraint=0       
                    
        #check cols
        for col in list(zip(*self.board)):
            domain=set(INITIAL_DOMAIN)
            
            numbers=Sudoku.__toNumbersSet(col)
            
            satisfied_constraint+=9-len(domain-numbers)
                    
        #check squares
        for row_start in range(0,8,3):
            for col_start in range(0,8,3):
                
                numbers=Sudoku.__toNumbersSet(self.__square(row_start,col_start))
                domain=set(INITIAL_DOMAIN)
            
                satisfied_constraint+=9-len(domain-numbers)
            
        self.satisfied_constraint=satisfied_constraint      
    
    def __randomizeSudokuAndScore(self):
    
        board=self.board
        for r in range(9):
            #initialization of row domain
            domain=list(INITIAL_DOMAIN)
            
            #remove values from domain already set in row
            for c in range(9):
                if not board[r][c].isEmpty:
                    domain.remove(board[r][c].value)
            
            #for each empty cell choose a random value to assign to it and remove that value from the domain.
            for c in range(9):
                if board[r][c].isEmpty:
                    board[r][c].value=choice(domain)
                    domain.remove(board[r][c].value)
        
        #calculate score for generated sudoku
        self.__fitness()

    """
    def numberFullCell(self):
        full_cells=0
        for row in range(9):
            for col in range(9):
                if not self.board[row][col].isEmpty:
                    full_cells+=1
        return full_cells
    """    
    
    @staticmethod
    def __getChild(parent1:Sudoku,parent2:Sudoku)->Sudoku:
        
        child=Sudoku()
        
        #at least one row from parent1 and at least one row from parent 2
        crossover_row_index=randint(1,8)
            
        for index in range(crossover_row_index):
            for c in range(9):
                
                cell=Cell(index,c,parent1.board[index][c].value)
                
                cell.isEmpty=parent1.board[index][c].isEmpty
                
                child.board[index].append(cell)
        
        for index in range(crossover_row_index,9):
            for c in range(9):
                
                cell=Cell(index,c,parent2.board[index][c].value)
                
                cell.isEmpty=parent2.board[index][c].isEmpty   
                
                child.board[index].append(cell)
        
        child.__fitness()
        
        return child
        
                            
    def __mutation(self,n_rows,n_cells_per_row):
        
        for _ in range(n_rows):
            
            #select a random row
            mutation_row_index=randint(0,8)
            mutation_row=self.board[mutation_row_index]
            
            for _ in range(n_cells_per_row):
                
                #from all possible indexes remove the indexes of the full cells
                indexes=[x for x in range(9)]
                for n,cell in enumerate(mutation_row):
                    if not cell.isEmpty:
                        indexes.remove(n)
                
                #sample 2 random indexes    
                cell1,cell2=sample(indexes,2)
                
                #swap
                temp=mutation_row[cell1]
                mutation_row[cell1]=mutation_row[cell2]
                mutation_row[cell2]=temp
                
                self.__fitness()
        
    @staticmethod
    def __isSolution(population:list[Sudoku])->Sudoku:
        for s in population:
            if s.satisfied_constraint==(81*2):
                return s
        return None
                                  
    def sudokuSolverGA(self, population_size:int=3000, selection_rate:float=0.25, random_selection_rate:float=0.25, n_children:int=4, mutation_rate:float=0.3, n_rows_swap:int=3, n_cells_per_row_swap:int=1, n_generations_no_improvement:int=30):
        
        iteration=1
        
        while True:
            
            #initial generation
            old_population=[Sudoku(self) for x in range(population_size)]
            for sudoku in old_population:
                sudoku.__randomizeSudokuAndScore()
            
            solution=Sudoku.__isSolution(old_population)
            if solution is not None:
                print("solution found at initial generation (generation 0)")
                self.board=copy.deepcopy(solution)
                self.finished=True
                return 0,0
            
            generation=1
            
            restart=0
            
            best_fit=max(old_population,key=operator.attrgetter("satisfied_constraint")).satisfied_constraint
                    
            while True:
                
                #random selection
                population=sample(old_population,int(population_size*random_selection_rate))
                
                #selection    
                old_population.sort(key=operator.attrgetter("satisfied_constraint"),reverse=True)
                
                for x in range(int(population_size*selection_rate)):
                    population.append(old_population[x])
                    
                #shuffle(population)
                
                #roulette wheel selection (fail)
                """
                sum_satisfied_constraints=sum([sudoku.satisfied_constraint for sudoku in old_population])
                p=[sudoku.satisfied_constraint/sum_satisfied_constraints for sudoku in old_population]
                population=np.random.choice(old_population,int(0.5*population_size),p=p,replace=True).tolist()
                """
                
                new_population=[copy.deepcopy(s) for s in population]
                
                while(len(new_population)<population_size):
                
                    children=[]
                        
                    parent1,parent2=sample(population,k=2)

                    for _ in range(n_children):
                        
                        
                        child=Sudoku.__getChild(parent1,parent2)    
                        
                        #children.append(max([child,parent1,parent2], key=operator.attrgetter("satisfied_constraint")))
                        children.append(child)    
                        
                    new_population+=children
                
                shuffle(new_population)
                
                for e in range(int(population_size*mutation_rate)):
                    new_population[e].__mutation(n_rows_swap,n_cells_per_row_swap)
                    
                shuffle(new_population)
                
                fit=max(new_population,key=operator.attrgetter("satisfied_constraint")).satisfied_constraint
                
                
                print("max:",fit,"/ 162 ",
                      "average:", "{:3.2f}".format(sum([x.satisfied_constraint for x in new_population])/len(new_population)),
                      " generation:",generation,
                      " restart: ",restart )
                
                
                solution=Sudoku.__isSolution(new_population)
                if solution is not None:
                    print("\nsolution found at regeneration "+str(iteration)+" at generation "+str(generation))
                    self.board=copy.deepcopy(solution.board)
                    self.finished=True
                    return restart,generation
                
                if fit>best_fit:
                    best_fit=fit
                    restart=0
                
                old_population=new_population
                generation+=1
                
                restart+=1
                
                if restart>n_generations_no_improvement:
                    
                    iteration+=1
                    
                    print("\nreached a possible local minimum")
                    
                    print("best solution for this iteration: ")
                    print(max(new_population,key=operator.attrgetter("satisfied_constraint")))
                    print(max(new_population,key=operator.attrgetter("satisfied_constraint")).checkSudoku())
                    
                    print("\nrestarting... ")
                    
                    del population,new_population,old_population,children,child,parent1,parent2
                    gc.collect()
                    break  