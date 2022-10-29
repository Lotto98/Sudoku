from Sudoku import *

def main():
    sudoku=Sudoku("solved/easy1_.txt")
    sudoku.printSudoku()
    sudoku.sudokuSolver()
    sudoku.printSudoku()
    sudoku.checkSudoku()

if __name__ == "__main__":
    main()