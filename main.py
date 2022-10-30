import sys
from Sudoku import *

def main():
    sudoku=Sudoku("examples/hard/hard1.txt")
    sudoku.printSudoku()
    sudoku.sudokuSolverCP()
    sudoku.printSudoku()
    print(sudoku.checkSudoku())

if __name__ == "__main__":
    main()