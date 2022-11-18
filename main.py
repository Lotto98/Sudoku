import sys
from Sudoku import *
from solver import sudokuSolverGA_NP
    
def test():
    
    if len(sys.argv)<5:
        print("Expected 4 parameters:\n1) type of computation (CP or GA)\n2) sudoku names (easy,normal,medium or hard)\n3) number \n4) n test")
        return
    
    _,type,name,i,n_test=sys.argv
    
    if name not in ["easy","medium","normal","hard"]:
        print("wrong sudoku name")
        return
        
    if type not in ["CP","GA"]:
        print("wrong computation type")
        return
    
    try:
        n_test=int(n_test)
    except:
        print("parameter 4 is not a number")
        return
     
    execution_times=[]
    
    for _ in range(n_test):
        
        pathIN="examples/"+name+"/"+name+i+".txt"
        sudoku=Sudoku(pathIN)
        
        start_time = time.perf_counter()
        
        if type=="CP":
            print("backtracked nodes",sudoku.sudokuSolverCP())
        elif type=="GA":
            restart,generation=sudoku.sudokuSolverGA()
            print(restart,generation)
            
        end_time = time.perf_counter()
        
        execution_time = end_time - start_time
        execution_times.append(execution_time)
        
        print(sudoku.checkSudoku())
        
    print(np.mean(execution_times))
    
def main():
    
    test()

    """
    path="examples/easy/easy1.txt"
        
    sudoku=Sudoku(path)
    
    print(sudoku,end='\n\n')
    
    sudoku.sudokuSolverCP()
    #sudoku.sudokuSolverGA()
    
    print(sudoku)
    print(sudoku.checkSudoku())
    """
if __name__ == "__main__":
    main()