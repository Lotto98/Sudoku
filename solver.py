from Cell import *
from Sudoku import *
        
    
            
def constraintsPropagation(sudoku: list[list[Cell]]):
    for r in range(0,9):
        row_numb=[cell.value for cell in sudoku[r]]
        
        for c in range(0,9):
            col_numb=[cell.value for cell in list(zip(*sudoku))[c]]
            
            if sudoku[r][c].value==0:
                
                sqr_numb=square(sudoku,whichSquare(r),whichSquare(c))
                
                sudoku[r][c].removeDomain(row_numb)
                sudoku[r][c].removeDomain(col_numb)
                sudoku[r][c].removeDomain(sqr_numb)
                
                print("domain "+str(sudoku[r][c].domain)+" for cell "+str(r)+","+str(c))
                
                if len(sudoku[r][c].domain)==1:
                    sudoku[r][c].value=sudoku[r][c].domain[0]
                    
                
                