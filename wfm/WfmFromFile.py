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
    attr=dict()
    proj=None
    state = 0
    count = 0
    for line in f.readlines():
        wds = line.strip().split()
        # print "#####", wds
        if len(wds) == 1 and wds[0] == "#END":
            state = 0
        elif len(wds) == 2 and wds[1] == "ATTR":
            state = 2
        elif len(wds) == 3 and wds[0] == "#BEGIN":
            n = int(wds[2])
            if wds[1] == "TOPO":
                if matrix:
                    mat = [[0 for j in range(n)] for i in range(n)]
                else: 
                    lnk = [[] for i in range(n)]
                state = 1
                count = 0
            elif wds[1] == "PROJ":
                proj = [set() for i in range(n)]
                state = 3
                count = 0
        elif state == 1: #read dependency
            if matrix:
                for s in wds:
                    mat[count][int(s)]=1
            else:
                for s in wds:
                    lnk[count]+=[int(s)]
            count=count+1
        elif state == 2: #read attributes
            if len(wds)>=2:             
                key=(int(wds[0]), wds[1])
                val=str()
                for w in wds[2:]:
                    val+=w+" "
                attr[key]=val
        elif state == 3: #read projection
            proj[count]=set([int(s) for s in wds])
            count=count+1
            # print proj
        else:
            print "### incorrect file format: lastread = ", line
            # print proj

    f.close()
    if matrix:
        return (mat, attr, True, proj)
    else:
        return (lnk, attr, False, proj)

if __name__ == "__main__":
    print wfmObjectFromFile("../data/sample.wfm", True)

