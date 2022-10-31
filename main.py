from Sudoku import *

def main():
    
    l=[]
    l.append(str)
    #CP and backtracking sudoku solver
    sudoku=Sudoku("examples/hard/hard1.txt")
    
    print(sudoku,end='\n\n')
    
    #sudoku.sudokuSolverCP()
    sudoku.sudokuSolverGA()
    
    #print(sudoku.fitness())
    
    print(sudoku)
    
    print(sudoku.checkSudoku())

if __name__ == "__main__":
    main()