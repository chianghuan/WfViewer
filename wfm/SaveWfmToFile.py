import sys

sys.path.append('../algor')

from GraphTran import *

def wfmObjectToFile(fpath, wfm):
    mat, attr, isMatrix, proj = wfm    
    try:
        f = open(fpath, 'w')
    except Exception, inst:
        print "### cannot write file:", fpath
        print str(inst)
        return
    # write contents to file
    if isMatrix == False and mat != None:
        mat = getMatrixFromLnk(mat)
    if mat != None:
        n = len(mat)
        f.write('#BEGIN TOPO %d\n' % n)
        for i in range(n):
            for j in range(n):
                if mat[i][j] == 1:
                    f.write(str(j) + ' ')
            f.write('\n')
        f.write('#END\n')
    if attr != None:
        #TODO
        pass
    if proj != None:
        f.write('#BEGIN PROJ %d\n' % len(proj))
        for x in proj:
            for y in x:
                f.write(str(y) + ' ')
            f.write('\n')
        f.write('#END\n')
