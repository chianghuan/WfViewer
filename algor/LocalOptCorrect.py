from GraphTran import *
from Soundness import *
from WfmFromProj import *

def weakOptimalCorrect(graph):
    if graph == None:
        return
    g, attr, isMatrix, proj = graph
    if isMatrix == False:
        g = getMatrixFromLnk(g)

    n = len(g)
    m = n - 1
    proj = [set([i]) for i in range(n)]

    tg = (g, attr, True, proj)
    changed = True
    while changed == True:
        changed = False
        tmppj = [set([i]) for i in range(m+1)]
        for i in range(1, m):
            if changed == True:
                break
            for j in range(i+1, m):
                if changed == True:
                    break
                if weakCanMerge(tg[0], i, j):
                    changed = True
                    proj[i] = proj[i] | proj[j]
                    del proj[j]
                    tmppj[i] = tmppj[i] | tmppj[j]
                    del tmppj[j]
                    tg = (tg[0], tg[1], tg[2], tmppj)
                    tg = wfmObjectFromProj(tg, True)
                    m = m-1
    return wfmObjectFromProj((g, attr, True, proj), True)

def strongOptimalCorrect():
    pass #TODO

def weakCanMerge(mat, a, b):
    a2b = b2a = False
    a_in = a_out = b_in = b_out = False
    if mat[a][b] == 1:
        a2b = True
    if mat[b][a] == 1:
        b2a = True
    n = len(mat)
    for i in range(n):
        if mat[a][i] == 1 and i!=b:
            a_out = True
        if mat[b][i] == 1 and i!=a:
            b_out = True
        if mat[i][a] == 1 and i!=b:
            a_in = True
        if mat[i][b] == 1 and i!=a:
            b_in = True


    if b2a == False and a_out == True and b_in == True:
        return False
    if a2b == False and b_out == True and a_in == True:
        return False
    return True
