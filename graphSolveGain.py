import sympy as sp
from Maison import *
import Structs

def SolveFinalGain (matrix):
    inp=[];
    n = len(matrix)
    counter=0;
    for i in range(n):
        for j in range(n):
            if(matrix[i][j]=='0'):
                 continue;
            inp.append([counter,i,j,int(matrix[i][j])]);
            counter+=1;
    print(inp);
    test=Maison();
    print()
    a=test.mason(0,n-1,inp);
    if(a=="Infinity"):
        return str(a)
    if(a==None):
        return str("No Path Found")
    return str(a)

