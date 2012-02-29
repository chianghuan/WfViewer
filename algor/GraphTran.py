#!/usr/bin/python27
import sys

def getMatrixFromLnk(graph):
    n = len(graph)
    mat = [[0 for j in range(n)] for i in range(n)]

    for i in range(n):
        for k in graph[i]:
            mat[i][k]=1

    return mat

def getLnkFromMatrix(graph):
    n = len(graph)
    lnk = [[] for i in range(n)]

    for i in range(n):
        for k in range(n):
            if graph[i][k] == 1:
                lnk[i] += [k]

    return lnk
