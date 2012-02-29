#!/usr/bin/python27
import sys

sys.path.append("../algor")

from GraphTran import *

def wfmObjectFromProj(wfm, matrix=False):
    if wfm==None or wfm[0]==None or wfm[3]==None:
        return None

    n=len(wfm[0]) # wfm size
    m=len(wfm[3]) # view size

    mat=[[0 for i in range(m)] for j in range(m)]
    for i in range(m):
        for j in range(m):
            k=0
            if wfm[2]==True: # matrix
                for p in wfm[3][i]:
                    if k == 1:
                        break
                    for q in range(n):
                        if k == 1:
                            break
                        if wfm[0][p][q]==1 and \
                        q in wfm[3][j]:
                            k = 1
            else: # link list
                for p in wfm[3][i]:
                    if k == 1:
                        break
                    for q in wfm[0][p]:
                        if k == 1:
                            break
                        if q in wfm[3][j]:
                            k = 1
            mat[i][j]=k

    if matrix==True:
        return (mat, None, True, wfm[3])
    else:
        return (getLnkFromMatrix(mat), None, False, wfm[3])
