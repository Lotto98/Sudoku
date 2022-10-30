import sys
from Sudoku import *

def main():
    
    #CP and backtracking sudoku solver
    sudoku=Sudoku("examples/hard/hard5.txt")
    
    sudoku.printSudoku()
    
    sudoku.sudokuSolverCP()
    
    sudoku.printSudoku()
    
    print(sudoku.checkSudoku())

if __name__ == "__main__":
    main()