import sys
from Sudoku import *
from solver import sudokuSolverGA_NP
    
def test():
    
    if len(sys.argv)<3:
        print("Expected 2 parameters:\n1) type of computation (CP or GA)\n2) sudoku names (easy,normal,medium or hard)\n3)start number\n4)end number")
        return
    
    _,type,name,start,end=sys.argv
    
    if name not in ["easy","medium","normal","hard"]:
        print("wrong sudoku name")
        return
        
    if type not in ["CP","GA"]:
        print("wrong computation type")
        return
    
    try:
        start=int(start)
        if start < 1:
            print("parameter 3 needs to be at least 1")
            return
    except:
        print("parameter 3 is not a number")
        return
    
    try:
        end=int(end)+1
    except:
        print("parameter 4 is not a number")
        return
    
    f=open("examples/"+name+"/results.txt","w")
    
    for i in range(start,end):
        
        pathIN="examples/"+name+"/"+name+str(i)+".txt"
        sudoku=Sudoku(pathIN)
        
        start_time = time.perf_counter()
        
        if type=="CP":
            sudoku.sudokuSolverCP()
        elif type=="GA":
            sudoku.sudokuSolverGA()
        
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        
        print(sudoku.checkSudoku(),execution_time)
        
        pathOUT="examples/"+name+"/sol_"+name+str(i)+".txt"
        sudoku.toFile(pathOUT)
        
        f.write(name+str(i)+": "+str(execution_time)+" s\n")
    
    f.close()
    
def main():
    
    test()
    
    """
    path="examples/normal/normal1.txt"
    
    sudoku=Sudoku(path)
    
    print(sudoku,end='\n\n')
    
    #sudoku.sudokuSolverCP()
    sudoku.sudokuSolverGA()
    
    print(sudoku)
    """

if __name__ == "__main__":
    main()