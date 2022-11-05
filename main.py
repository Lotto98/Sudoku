import threading
from Sudoku import *
from solver import sudokuSolverGA_NP
    
            
def main():
    
    path="examples/normal/normal1.txt"
    
    #CP and backtracking sudoku solver
    sudoku=Sudoku(path)
    
    print(sudoku,end='\n\n')
    
    #sudoku.sudokuSolverCP()
    sudoku.sudokuSolverGA()
    #sudokuSolverGA_NP(sudoku)
    #sudoku=multithread(path,5)
    
    print(sudoku)
    
    print(sudoku.checkSudoku())

if __name__ == "__main__":
    main()