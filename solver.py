from Cell import *
from tabulate import tabulate

def createSudoku(filename: str):
    sudoku=[]
    with open(filename) as file:
        for i,line in enumerate(file):
            line=line[:-1]
            row=[]
            sudoku.append(row)
            for j,x in enumerate(line):
                if x==0:
                    row.append(EmptyCell(_i=i,_j=j))
                else:
                    row.append(FullCell(_value=x,_i=i,_j=j))
    return sudoku

def printSudoku(sudoku:list[list[Cell]]):
    print(tabulate(sudoku,headers="keys",showindex=True,tablefmt="outline"))

def checkDigits(l: list[Cell]):
    
    domain=list(INITIAL_DOMAIN)
    
    for e in l:
        x=e.value
        if x>9 or x<1:
            print("outside domain boundaries",end='')
            return False
        
        try:
            domain.remove(x)
        except:
            print("multiple occorences of same number ("+str(x)+")",end='')
            return False;
    
    if len(domain)!=0:
        print("digits: "+domain+" not present",end='')
        return False
    return True

def checkSquare(sudoku:list[list[Cell]], i:int, j:int):
    l=[]
    for r in range(i,i+3):
        for c in range(j,j+3):
            l.append(sudoku[r][c])
    return checkDigits(l)            
        
def checkSudoku(sudoku:list[list[Cell]]):
    #check rows
    for n,row in enumerate(sudoku):
        if not checkDigits(row):
            print(" in row "+str(n))
            return False
    #check cols
    for n,col in enumerate(list(zip(*sudoku))[1:]):
        if not checkDigits(col):
            print(" in col "+str(n))
            return False
    #check squares
    for row_start in range(0,8,3):
        for col_start in range(0,8,3):
            if not checkSquare(sudoku,row_start,col_start):
                print(" in square: "+str(row_start)+","+str(col_start))
                return False
    return True

def main():
    sudoku=createSudoku("solved/easy1.txt")
    printSudoku(sudoku)
    print(checkSudoku(sudoku))

if __name__ == "__main__":
    main()