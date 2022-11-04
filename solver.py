from Sudoku import Sudoku,INITIAL_DOMAIN

def fitness(sudoku:np.ndarray,mask:np.ndarray):
    
    satisfied_constraint=0    
                
    #check cols
    for col in range(9):
        domain=set(INITIAL_DOMAIN)
        
        numbers=sudoku.
        
        satisfied_constraint+=9-len(domain-numbers)
                
    #check squares
    for row_start in range(0,8,3):
        for col_start in range(0,8,3):
            
            numbers=Sudoku.__toNumbersSet(self.__square(row_start,col_start))
            domain=set(INITIAL_DOMAIN)
        
            satisfied_constraint+=9-len(domain-numbers)
        
    self.satisfied_constraint=satisfied_constraint
    
def randomizeSudoku(sudoku:np.ndarray,mask:np.ndarray):

    for r in range(9):
        #initialization of row domain
        domain=list(INITIAL_DOMAIN)
        
        #remove values from domain already set in row
        for c in range(9):
            if mask[r*9+c]:
                domain.remove(sudoku[r*9+c])
        
        #for each empty cell choose a random value to assign to it and remove that value from the domain.
        for c in range(9):
            if mask[r*9+c]:
                sudoku[r*9+c]=choice(domain)
                domain.remove(sudoku[r*9+c])
    
    #calculate score for generated sudoku
    fitness()
    

def sudokuSolverGA_NP(self,population_size:int=2000, selection_rate:float=0.25, random_selection_rate:float=0.25, n_children:int=4, mutation_rate:float=0.3, n_generations_no_improvement:int=30):
    
    sudoku,mask=self.toNumpy()
    
    iteration=1

    while True:
        
        #initial generation
        
        sudokus=[sudoku.copy() for _ in range(population_size)]
        
        old_population=[]
        
        for s in sudokus:
            score=Sudoku.randomizeSudokus(s,mask)
            old_population.append((s,score))
        
        solution=Sudoku.isSolution(old_population)
        if solution is not None:
            print("solution found at initial generation (generation 0)")
            self.sudoku=copy.deepcopy(solution)
            return
    