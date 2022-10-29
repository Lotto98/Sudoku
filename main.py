import sys
from Sudoku import *

def main():
    sudoku=Sudoku("examples/hard/hard1.txt")
    #sudoku.printSudoku()
    sudoku.sudokuSolver()
    
    sudoku.printSudoku()
    print(sudoku.checkSudoku())
    
def recursive_function(n, sum):
    if n < 1:
        return sum
    else:
        return recursive_function(n-1, sum+n)

if __name__ == "__main__":
    main()