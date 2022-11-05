import time
from Sudoku import Sudoku,INITIAL_DOMAIN,np
import copy

def fitnessNP(board:np.ndarray):
        
    satisfied_constraint=0
    
    #check cols
    for c in range(9):
        
        numbers=board.transpose()[c].flatten()
        domain=np.array(list(INITIAL_DOMAIN),dtype=int)
        
        satisfied_constraint+=9-np.setdiff1d(domain,numbers).size
    
    #check squares
    for row_start in range(0,8,3):
        for col_start in range(0,8,3):
                    
            numbers=np.array([],dtype=int)
            
            for r in range(3):
                for c in range(3):
                    numbers=np.append(numbers,board[row_start+r][col_start+c])
            
            domain=np.array(list(INITIAL_DOMAIN),dtype=int)
                
            satisfied_constraint+=9-np.setdiff1d(domain,numbers).size
        
    return satisfied_constraint
            
def randomizeSudokuNP(initial_board:np.ndarray,mask:np.ndarray):
    
    board=np.array(initial_board)
    
    for r in range(9):
        
        #initialization of row domain
        domain=list(INITIAL_DOMAIN)
        
        #remove values from domain already set in row
        for c in range(9):
            if not mask[r][c]:
                domain.remove(initial_board[r][c])
        
        #for each empty cell choose a random value to assign to it and remove that value from the domain.
        for c in range(9):
            if mask[r][c]:
                board[r][c]=np.random.choice(domain,size=1)
                domain.remove(board[r][c])
    
    return board

def isSolution(population:np.ndarray,population_score:np.ndarray):
    
    max_index=np.argmax(population_score)
    
    if population_score[max_index]==(81*2):
        return population[max_index]
    else:
        return None

def getChild(parent1:np.ndarray,parent2:np.ndarray)->np.ndarray:
        
    child=copy.deepcopy(parent2)
    
    #at least one row from parent1 and at least one row from parent 2
    crossover_row_index=np.random.randint(1,9)
        
    for r in range(crossover_row_index):
        child[r]=copy.deepcopy(parent1[r])
    
    return child

def mutation(board:np.ndarray,mask:np.ndarray):
    
    #select a random row
    mutation_row_index=np.random.randint(0,9)
    mutation_row=board[mutation_row_index]
    
    #from all possible indexes remove the indexes of the full cells
    indexes=[x for x in range(9)]
    for index in range(9):
        if not mask[mutation_row_index][index]:
            indexes.remove(index)
    
    #sample 2 random indexes    
    cell1,cell2=np.random.choice(indexes,2)
    
    #swap
    temp=mutation_row[cell1]
    mutation_row[cell1]=mutation_row[cell2]
    mutation_row[cell2]=temp
    
def sudokuSolverGA_NP(sudoku:Sudoku,population_size:int=2000, selection_rate:float=0.25, random_selection_rate:float=0.25, n_children:int=4, mutation_prob:float=0.3, n_generations_no_improvement:int=30):
    
    board,mask=sudoku.toNumpy()
    
    iteration=1
        
    while True:
        
        start_time = time.perf_counter()
        
        #initial generation
        old_population=np.array([randomizeSudokuNP(board,mask) for _ in range(population_size)])
        old_population_score=np.array([fitnessNP(board) for board in old_population])
        
        solution=isSolution(old_population,old_population_score)
        if solution is not None:
            print("solution found at initial generation (generation 0)")
            return solution
        
        generation=1
        
        restart=0
        
        best_fit=max(old_population_score)
                
        while True:
            
            #random selection
            random_indexes=np.random.randint(0,population_size,size=int(population_size*random_selection_rate))
            
            population=old_population[random_indexes]
            population_score=old_population_score[random_indexes]
            
            #selection    
            sort_indexes=np.argsort(old_population_score)
            
            old_population=old_population[sort_indexes][::-1]
            old_population_score=np.sort(old_population_score)[::-1]
            
            old_population=old_population[:int(population_size*selection_rate)]
            old_population_score=old_population_score[:int(population_size*selection_rate)]
            
            population=np.append(population,old_population,axis=0)
            population_score=np.append(population_score,old_population_score,axis=0)
            
            
            #new generation
            new_population=copy.deepcopy(population)
            new_population_score=copy.deepcopy(population_score)
            
            while(new_population.shape[0]<population_size):
            
                children=np.array([],dtype=int).reshape(0,9,9)
                children_score=np.array([], dtype=int)
                    
                parents=population[np.random.randint(0,population.shape[0],size=2)]

                for _ in range(n_children):
                    
                    child=getChild(parents[0],parents[1])    
                    
                    children=np.append(children,child.reshape(1,9,9),axis=0)
                    children_score=np.append(children_score,fitnessNP(child))      
                    
                new_population=np.append(new_population,children,axis=0)
                new_population_score=np.append(new_population_score,children_score)
            
            #mutation
            for index in range(population_size):
                r=np.random.random_sample()
                if r<=mutation_prob:
                    mutation(new_population[index],mask)
                    new_population_score[index]=fitnessNP(new_population[index])
            
            fit=max(new_population_score)
            
            print("max:",fit,"/ 162 ",
                " generation:",generation,
                " restart: ",restart )
            
            solution=isSolution(new_population,new_population_score)
            if solution is not None:
                print("\nsolution found at regeneration "+str(iteration)+" at generation "+str(generation))
                return solution
            
            if fit>best_fit:
                best_fit=fit
                restart=0
            
            old_population=new_population
            old_population_score=new_population_score
            
            generation+=1
            
            restart+=1
            
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            print(f"The execution time is: {execution_time}")
            
            if restart>n_generations_no_improvement:
                
                iteration+=1
                
                print("\nreached a possible local minimum")
                
                print("best solution for this iteration: ")
                #print(max(new_population,key=operator.attrgetter("satisfied_constraint")))
                #print(max(new_population,key=operator.attrgetter("satisfied_constraint")).checkSudoku())
                
                print("\nrestarting... ")
                
                break 
    