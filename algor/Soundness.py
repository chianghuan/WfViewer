import sys
from GraphTran import *

def isViewSound(graph, attr, isMatrix, proj):
    unsound=[]
    ret = True
    for i, subset in enumerate(proj):
        if False == isViewNodeSound(graph, isMatrix, subset):
            unsound.append(i)
            ret = False
    return ret, unsound

def isViewNodeSound(graph, isMatrix, subset):
    mat = graph
    if isMatrix == False:
        mat = getMatrixFromLnk(graph)
    inset, outset = getInOutSet(mat, subset)
 
    for k in subset:
        for i in subset:
            for j in subset:
                if mat[i][k] == 1 and mat[k][j] == 1:
                    mat[i][j] = 1

    for i in inset:
        for j in outset:
            if mat[i][j] != 1:
                return False
            
def getInOutSet(mat, subset):
    inset, outset = set(), set()
    n = len(mat)
    for i in range(n):
        if i not in subset:
            for j in range(n):
                if j in subset and mat[i][j] == 1:
                    inset.add(j)
                if j in subset and mat[j][i] == 1:
                    outset.add(j)

    return inset, outset
