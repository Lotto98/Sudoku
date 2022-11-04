from __future__ import annotations
import gc
import operator
from Cell import Cell,INITIAL_DOMAIN

import numpy as np

import copy

from queue import LifoQueue

from random import randint,choice, sample,shuffle
from typing import Counter

from tabulate import tabulate

class Sudoku:
    def __init__(self,_sudoku=None):
        """
        Create a sudoku object from a file or from another sudoku object.

        Args:
            _sudoku (str or Sudoku): .
        """
        if _sudoku is None:
            self.sudoku=[[] for x in range(9)]
        elif isinstance(_sudoku,str):
            self.sudoku=[]
            try:
                with open(_sudoku) as file:
                    for i,line in enumerate(file):
                        line=line.strip('\n')
                        row=[]
                        self.sudoku.append(row)
                        for j,x in enumerate(line):
                            if int(x)==0:
                                row.append(Cell(i,j))
                            else:
                                row.append(Cell(i,j,_value=int(x)))
            except FileNotFoundError as fnf_error:
                print(fnf_error)
        
        elif isinstance(_sudoku,Sudoku):
            self.sudoku=copy.deepcopy(_sudoku.sudoku)
        else:
            raise TypeError("Expected a str or sudoku object, found "+str(type(_sudoku)))
    
    def __str__(self):
        """
        Function that prints sudoku as a matrix of a better visualization.
        """
        print()
        
        if len(self.sudoku)!=9:
            print("Warning: malformed sudoku, number of rows is not 9")
            
        for n,row in enumerate(self.sudoku):
            if len(row)!=9:
                print("Warning: malformed sudoku in row "+str(n))
        
        return tabulate(self.sudoku ,headers="keys",showindex=True,tablefmt="outline")

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
                l.append(self.sudoku[r][c])
        return l            
        
    def checkSudoku(self):
        """
        Function that checks the sudoku correctness.

        Returns:
            bool: 'True' if the sudoku is correct, 'False' otherwise.
        """
        #check rows
        for n,row in enumerate(self.sudoku):
            if not self.__checkDigits(row):
                print(" in row "+str(n))
                return False
        #check cols
        for n,col in enumerate(list(zip(*self.sudoku))):
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
        Sudoku solver with CP and backtracking approach.
        """
        
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
                
                #1) reset visited domain for min domain cell
                min_cell.visitedDomain=set()
                
                #2) get last visited cell and the cell in which the domain was modified by its assignment
                last_visited_cell,domainRemovedCells=visited_cells.get()
                
                #3) update last visited cell to a empty cell
                last_visited_cell.isEmpty=True
                
                #4) add the value previously assigned to the last visited cell to the cells previously modified by its assignment
                for cell in domainRemovedCells:
                    cell.addDomain(last_visited_cell.value)
                
                #5) set the min domain cell as the last visited cell to explore the next value of its domain
                min_cell=last_visited_cell
    
    def toNumpy(self):
        
        sudoku_values=[]
        mask=[]
        
        for row in self.sudoku:
            for cell in row:
                sudoku_values.append(cell.value)
                if cell.isEmpty:
                    mask.append(True)
                else:
                    mask.append(False)
        
        return np.array(sudoku_values,),np.array(mask)
    
        
    """
    @staticmethod
    def __toNumbersList(l:list[Cell])->list[int]:
        
        return [cell.value for cell in l]
    
    def __fitness(self):
        
        duplicates=0
            
        #check cols
        for col in list(zip(*self.sudoku)):
            
            numbers=Sudoku.__toNumbersList(col)
            
            for value in dict(Counter(numbers)).values():
                    duplicates+=value-1
                    
        #check squares
        for row_start in range(0,8,3):
            for col_start in range(0,8,3):
                
                numbers=Sudoku.__toNumbersList(self.__square(row_start,col_start))
                    
                for value in dict(Counter(numbers)).values():
                    duplicates+=value-1
            
        self.duplicates=duplicates
        
        #print(self)
        #print(duplicates)
        
        return duplicates==0
        
    def randomizeSudokuAndScore(self):
        board=self.sudoku
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
                    #board[r][c].isEmpty=False
                    domain.remove(board[r][c].value)
        
        #calculate score for generated sudoku
        self.__fitness()
        
    def __addNRandomRows(self, parent1: Sudoku, parent2: Sudoku):
        
        #at least one row from parent1 and at least one row from parent 2
        crossover_row_index=randint(1,8)
            
        for index in range(crossover_row_index):    
            self.sudoku[index]=parent1.sudoku[index]
        
        for index in range(crossover_row_index,9):
            self.sudoku[index]=parent2.sudoku[index]
            
    def __mutation(self):
        #select a random row
        mutation_row_index=randint(0,8)
        mutation_row=self.sudoku[mutation_row_index]
        
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
        
        #update row
        self.sudoku[mutation_row_index]=mutation_row
        
        return self.__fitness()
        
        
    def sudokuSolverGA(self, population_size:int=2000, selection_rate:float=0.25, random_selection_rate:float=0.25, n_children:int=4, mutation_rate:float=0.3, max__generations:int=1000, restart_after_n:int=50):
        
        generation=0
        
        while(generation<max__generations):
            
            #initial generation
            old_population=[Sudoku(self) for x in range(population_size)]
            
            for sudoku in old_population:
                sudoku.randomizeSudokuAndScore()
    
            found=False
            best_score=1000
            restart=0
            
            while (not found):
            
                #random selection
                population=sample(old_population,int(population_size*random_selection_rate))
                
                #selection    
                old_population.sort(key=operator.attrgetter("duplicates"))
                
                for x in range(int(population_size*selection_rate)):
                    population.append(old_population[x])
                    
                shuffle(population)
                
                children=[]
            
                parent1,parent2=sample(population,k=2)

                for e in range(n_children):
                    
                    child.__addNRandomRows(parent1, parent2)
                    
                    found=child.__fitness() or found

                    children.append(child)
                
                children.append(parent1)
                children.append(parent2)
                children.sort(key=operator.attrgetter("duplicates"))
                
                population.remove(parent1)
                population.remove(parent2)
                
                population.append(children[0])
                population.append(children[1])
                
                for e in range(int(population_size*mutation_rate)):
                    found=population[e].__mutation() or found
                
                print(min(population,key=lambda x:x.duplicates).duplicates)
                
                if min(population,key=operator.attrgetter("duplicates")).duplicates<best_score:
                    best_score=min(population,key=operator.attrgetter("duplicates")).duplicates
                    restart=0
                
                if restart>restart_after_n:
                    break
                
                generation+=1
                restart+=1
                old_population=population
            
            print("restarted")
            
"""
    @staticmethod
    def __toNumbersSet(l:list[Cell])->list[int]:
        
        return set([cell.value for cell in l])
    
    """
    def fitness(self):
        
        duplicates=0
        
        #check rows
        for row in self.sudoku:
            
            numbers=Sudoku.__toNumbersList(row)
            
            for value in dict(Counter(numbers)).values():
                    duplicates+=value-1
                    
        #check cols
        for col in list(zip(*self.sudoku)):
            
            numbers=Sudoku.__toNumbersList(col)
            
            for value in dict(Counter(numbers)).values():
                    duplicates+=value-1
                    
        #check squares
        for row_start in range(0,8,3):
            for col_start in range(0,8,3):
                
                numbers=Sudoku.__toNumbersList(self.__square(row_start,col_start))
                    
                for value in dict(Counter(numbers)).values():
                    duplicates+=value-1
            
        self.duplicates=duplicates
        """
    
    def fitness(self):
        
        satisfied_constraint=0
        
        """
        #check rows
        for row in self.sudoku:
            domain=set(INITIAL_DOMAIN)
            
            numbers=Sudoku.__toNumbersSet(row)
            
            satisfied_constraint+=9-len(domain-numbers)
        """        
                    
        #check cols
        for col in list(zip(*self.sudoku)):
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
        
                    
    
    def randomizeSudokuAndScore(self):
        """
        board=self.sudoku
        #for each empty cell choose a random value to assign to it
        for r in range(9): 
            for c in range(9):
                if board[r][c].isEmpty:
                    board[r][c].value=choice([x for x in range(1,10)])
        
        #calculate score for generated sudoku
        self.fitness()
        """
        board=self.sudoku
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
                    #board[r][c].isEmpty=False
                    domain.remove(board[r][c].value)
        
        #calculate score for generated sudoku
        self.fitness()

    def numberFullCell(self):
        full_cells=0
        for row in range(9):
            for col in range(9):
                if not self.sudoku[row][col].isEmpty:
                    full_cells+=1
        return full_cells
        
    
    @staticmethod
    def getChild(parent1:Sudoku,parent2:Sudoku)->Sudoku:
        
        """
        child=Sudoku()
        
        #get number of full cell to exclude them from crossover
        n_full_cells=parent1.numberFullCell()
        
        #at least one Cell from parent1 and at least one Cell from parent2 without counting full cells
        n_cells_fromParent1=randint(1,80-n_full_cells)
        
        #for each row
        for r in range(9):
            
            #create a row and append it to sudoku
            row=[]
            child.sudoku[r]=row
            
            #for each cell in row
            for c in range(9):
                
                #create cell and append it to row
                cell=Cell(r,c,0)
                row.append(cell)
                
                #if the cell is empty choose a cell from parent 1 or parent 2
                if parent1.sudoku[r][c].isEmpty:
                    
                    if n_cells_fromParent1>=0:
                        
                        cell.value=parent1.sudoku[r][c].value
                        n_cells_fromParent1-=1
                    else:
                        cell.value=parent2.sudoku[r][c].value
                        
                else:
                    #if the cell is full, simply copy it
                    cell.value=parent1.sudoku[r][c].value
                    cell.isEmpty=False
        
        child.fitness()
        
        return child
        """
        
        child=Sudoku()
        
        #at least one row from parent1 and at least one row from parent 2
        crossover_row_index=randint(1,8)
            
        for index in range(crossover_row_index):
            for c in range(9):
                
                cell=Cell(index,c,parent1.sudoku[index][c].value)
                
                cell.isEmpty=parent1.sudoku[index][c].isEmpty
                
                child.sudoku[index].append(cell)
        
        for index in range(crossover_row_index,9):
            for c in range(9):
                
                cell=Cell(index,c,parent2.sudoku[index][c].value)
                
                cell.isEmpty=parent2.sudoku[index][c].isEmpty   
                
                child.sudoku[index].append(cell)
        
        child.fitness()
        
        return child
        
                            
    def mutation(self):
        
        """
        indexes_domain=[(x,y) for x in range(9) for y in range(9)]
        
        indexes=sample(indexes_domain,k=n_mutated_cells)
        
        for r,c in indexes:
            self.sudoku[r][c].value=randint(1,9)
        
        self.fitness()
        """

        #select a random row
        mutation_row_index=randint(0,8)
        mutation_row=self.sudoku[mutation_row_index]
        
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
        
        self.fitness()
        
    @staticmethod
    def isSolution(population:list[Sudoku]):
        for s in population:
            if s.satisfied_constraint==(81*2):
                return s
        return None
                                  
    def sudokuSolverGA(self, population_size:int=1500, selection_rate:float=0.25, random_selection_rate:float=0.25, n_children:int=4, mutation_rate:float=0.4, n_mutation_swap:int=4, n_generations_no_improvement:int=50):
        
        iteration=1
        
        while True:
            
            #initial generation
            
            old_population=[Sudoku(self) for x in range(population_size)]
            for sudoku in old_population:
                sudoku.randomizeSudokuAndScore()
            
            solution=Sudoku.isSolution(old_population)
            if solution is not None:
                print("solution found at initial generation (generation 0)")
                self.sudoku=copy.deepcopy(solution)
                return
            
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
                    
                shuffle(population)
                
                
                new_population=[copy.deepcopy(s) for s in population]
                
                while(len(new_population)<population_size):
                
                    children=[]
                        
                    parent1,parent2=sample(population,k=2)

                    for _ in range(n_children):
                        
                        
                        child=Sudoku.getChild(parent1,parent2)    
                        
                        #children.append(max([child,parent1,parent2], key=operator.attrgetter("satisfied_constraint")))
                        children.append(child)    
                        
                    new_population+=children
                
                shuffle(new_population)
                
                for e in range(int(population_size*mutation_rate)):
                    for _ in range(n_mutation_swap):
                        new_population[e].mutation()
                    
                shuffle(new_population)
                
                fit=max(new_population,key=operator.attrgetter("satisfied_constraint")).satisfied_constraint
                
                print("max:",fit,"/ 162 ",
                      "average:", "{:3.2f}".format(sum([x.satisfied_constraint for x in new_population])/len(new_population)),
                      " generation:",generation,
                      " restart: ",restart )
                
                solution=Sudoku.isSolution(new_population)
                if solution is not None:
                    print("\nsolution found at regeneration "+str(iteration)+" at generation "+str(generation))
                    self.sudoku=copy.deepcopy(solution.sudoku)
                    return
                
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