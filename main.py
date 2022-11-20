import sys
from Sudoku import *
import time
    
def test():
    
    if len(sys.argv)!=4:
        print("Expected 4 parameters:\n1) type of computation (CP or GA)\n2) sudoku names (easy,normal,medium or hard)\n3) number")
        return
    
    _,type,name,i=sys.argv
    
    if name not in ["easy","medium","normal","hard"]:
        print("wrong sudoku name")
        return
        
    if type not in ["CP","GA"]:
        print("wrong computation type")
        return
    
    pathIN="examples/"+name+"/"+name+i+".txt"
    sudoku=Sudoku(pathIN)
    
    start_time = time.perf_counter()
    
    print("full cells",sudoku.countFullCells())
    
    if type=="CP":
        restored_nodes,assignments=sudoku.sudokuSolverCP()
        print("restored nodes",restored_nodes,"assignments",assignments)
    elif type=="GA":
        restart,generation=sudoku.sudokuSolverGA()
        print("restart",restart,"generation",generation)
    
    end_time = time.perf_counter()
    
    execution_time = end_time - start_time
    print("execution time",execution_time)
    
    print(sudoku.checkSudoku())
    
def main():
    
    #test()

    
    path="examples/easy/easy1.txt"
        
    sudoku=Sudoku(path)
    
    print(sudoku,end='\n\n')
    
    #sudoku.sudokuSolverCP()
    sudoku.sudokuSolverGA()
    
    print(sudoku)
    print(sudoku.checkSudoku())

if __name__ == "__main__":
    main()