#!/usr/bin/python27
import sys

sys.path.append('../algor')

from xml.etree import ElementTree
from GraphTran import *

def wfmObjectFromXML(fpath, matrix=False):
    di = dict()
    per = ElementTree.parse(fpath)
    n = 0
    for x in per.iter():
        if x.tag == 'STEPCLASS':
            n += 1
    n += 2
    mat = [[0 for i in range(n)] for j in range(n)]
    m = 1
    for x in per.iter():
        if x.tag == 'STEPCLASS':
            di[int(x.attrib['id'].strip())] = m
            if x.attrib['isUserInput'].strip() == 'true':
                mat[0][m] = 1
            if x.attrib['isUserOutput'].strip() == 'true':
                mat[m][n-1] = 1
            m += 1
    for x in per.iter():
        if x.tag == 'RELATION':
            fr = di[int(x.attrib['start'].strip())]
            to = di[int(x.attrib['stop'].strip())]
            mat[fr][to] = 1
    attr = dict()
    proj = None
    if matrix:
        return (mat, attr, True, proj)
    else:
        return (getLnkFromMatrix(mat), attr, False, proj)

if __name__ == '__main__':
    print wfmObjectFromXML('../data/sample.xml', True)
