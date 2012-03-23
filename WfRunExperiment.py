#!/usr/bin/python27 -u

import sys
import time
sys.path.append('./wfm')
sys.path.append('./algor')

from WfmFromFile import *
from WfmFromXML import *
from SaveWfmToFile import *

from Soundness import *
from LocalOptCorrect import *
from ExtAndComb import *

for i in range(1, 16):
    filename = './data/WF' + str(i) + '.xml'
    wfm = wfmObjectFromXML(filename, True)
    print filename, 
    print len(wfm[0]),
    t1 = time.time()
    view = extAndComb(wfm)
    t2 = time.time()
    print len(view[0]),
    print t2 - t1
    
print '#'*8

for i in range(1, 11):
    filename = './data/example' + str(i) + '.xml'
    wfm = wfmObjectFromXML(filename, True)
    print filename, 
    print len(wfm[0]),
    t1 = time.time()
    view = extAndComb(wfm)
    t2 = time.time()
    print len(view[0]),
    print t2 - t1
