#!/usr/bin/python27 

import sys, getopt
import random

def usage():
    print "usage: WfmGenerator n [OPTION]..."
    print "\tgenerates .wfm files, with n activities"
    print "\n\toptions:"
    print "\t-a: set to generate acycle graph workflow"
    print "\t-h: help"
    print "\t-T dir: generated file name of the workflow model"
    print "\n\t By huanchiang@gmail.com SIST sun-yat-sen university"

def generateMatrix(n, acyc=False):
    mat = [[random.randint(0, 3) for j in range(n)] for i in range(n)]
    """ node 0 is source and node n-1 is the converge"""
    for i in range(n):
        mat[i][0] = 1
        mat[n-1][i] = 1
    return mat

def writeWfmFile(mat, tpath):
    try:
        f = open(tpath, "w")
    except:
        print "cannot open file: ", tpath
    f.write("#BEGIN TOPO ")
    n = len(mat)
    f.write(str(n))
    f.write("\n")
    for i in range(n):
        for j in range(n):
            if mat[i][j] == 0:
                f.write(str(j))
                f.write(" ")
        f.write("\n")
    f.write("#END")
    f.close()
    
def generateWfm(n, tpath, acyc):
    mat = generateMatrix(n, acyc)
    writeWfmFile(mat, tpath)

if __name__ == "__main__" :    
    if len(sys.argv) < 2 :
        usage()
        sys.exit()

    opts, args = getopt.getopt(sys.argv[2:], "AhT:")

    acyc = False
    tpath = "../data/generated.wfm"

    for op, val in opts:
        if op == "-A":
            acyc = True
        elif op == "-T":
            tpath = val 
        elif op == "-h":
            usage()
        else:
            usage()
            sys.exit()

    generateWfm(int(sys.argv[1]), tpath, acyc)
