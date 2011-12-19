#!/usr/bin/python27
import sys

def wfmObjectFromFile(fpath, matrix=False):
    try:
        f = open(fpath, "r")
    except Exception, inst:
        print "### cannot open file:", fpath
        print str(inst)
        return [[]]

    mat=[[]]
    lnk=[[]]
    attr=[]
    state = 0
    count = 0
    for line in f.readlines():
        wds = line.strip().split()
        if len(wds) == 1 and wds[0] == "#END":
            state = 0
        elif len(wds) == 3 and wds[0] == "#BEGIN":
            n = int(wds[2])
            if wds[1] == "TOPO":
                if matrix:
                    mat = [[0 for j in range(n)] for i in range(n)]
                else: 
                    lnk = [[] for i in range(n)]
                state = 1
                count = 0
            elif wds[1] == "INFO":
                state = 2
        elif state == 1: #read dependency
            if matrix:
                for s in wds:
                    mat[count][int(s)]=1
            else:
                for s in wds:
                    lnk[count]+=[int(s)]
            count=count+1
        elif state == 2: #read attributes
            pass #TODO
        else:
            print "### incorrect file format"

    f.close()
    if matrix:
        return (mat, attr, True)
    else:
        return (lnk, attr, False)

if __name__ == "__main__":
    print wfmObjectFromFile("./sample.wfm", True)

