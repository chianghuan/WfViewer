from Soundness import *
from WfmFromProj import *
from GraphTran import *
from Queue import *
from copy import *

def back(g, v, mk, li, num, cur):
    mk[v] = 1
    cur.add(v)
    for u in range(len(g)):
        if mk[u] == -1 and g[u][v] == 1:
            num = back(g, u, mk, li, num, cur)
    return num

def dfs(g, u, mk, li, num):
    mk[u] = 1
    for v in range(len(g)):
        if mk[v] == -1 and g[u][v] == 1:
            num = dfs(g, v, mk, li, num)
    num = num - 1
    li[num] = u
    return num

def mergeSCC(graph):
    g, attr, isMatrix, proj = graph
    if isMatrix == False:
        g = getMatrixFromLnk(g)
    isMatrix = True

    li = [-1 for i in range(len(g)+1)]
    num = len(g) + 1
    mk = [-1 for i in range(len(g))]
    for i in range(len(g)):
        if mk[i] == -1:
            num = dfs(g, i, mk, li, num)
    mk = [-1 for i in range(len(g))]

    setli = []
    setli += [set()]
    curp = 0
    cur = setli[curp]

    for i in range(len(g)):
        if mk[li[i+1]] == -1:
            num = back(g, li[i+1], mk, li, num, cur)
            curp = curp + 1
            setli += [set()]
            cur = setli[curp]
            
    #TODO merge SCC

    return (g, attr, isMatrix, proj)

def extAndComb(graph):
    if graph == None:
        return

    graph = mergeSCC(graph)

    g, attr, isMatrix, proj = graph
    if isMatrix == False:
        g = getMatrixFromLnk(g)

    gt = copy(g)

    resproj = [[x] for x in range(0, len(g))]

    while True:
        # since there is still change
        if len(gt) <= 3:
            break
        retset = rettmp = None
        for i in range(1, len(gt) - 1):
            rettmp = extend(gt, i)
            if retset == None or (rettmp != None and len(rettmp) > len(retset)):
                retset = rettmp
        if retset == None:
            # no change
            break
        # get merge set
        ret = [ x for x in retset]
        ret.sort()
        for i in range(1, len(ret)):
            # combine the combinable nodes
            resproj[ret[0]] = resproj[ret[0]] + resproj[ret[i]]
        for i in range(len(ret) - 1, 0, -1):
            # delete the combined nodes
            del resproj[ret[i]]
        gt, attr, isMatrix, proj = wfmObjectFromProj((g, None, True, resproj), True)

    return wfmObjectFromProj((g, attr, True, resproj), True)

def extend(gm, st):
    n = len(gm)
    mx = 0
    ret = rettmp = None
    # extend the simple linear structure
    gm[st][st] = 0
    if gm[st].count(1) == 1:
        # if st has only one out-degree (except to END)
        tar = gm[st].index(1)
        if st != tar and tar != n-1:
            ret = set([st, tar]) 
    for i in range(1, n - 1):
        # for each edge (st, i)
        if gm[st][i] == 1 and i != st:
            tmp = [gm[x][i] for x in range(n)]
            tmp[i] = 0
            if tmp.count(1) == 1:
                #if i has only one in-degree (except from SRC)
                ret = set([st, i])
                break
    # try to extend a complete bipartite structure
    rettmp = spread(gm, st)
    if rettmp != None:
        return rettmp
    return ret

def spread(gm, st):
    q = Queue()
    inset = set()
    outset = set()
    markin = [0 for i in range(len(gm))]
    markout = [0 for i in range(len(gm))]
    markin[0] = markin[len(gm) - 1] = 1
    markout[0] = markout[len(gm) - 1] = 1
    n = len(gm)
    q.put((st, True)) # True for in, False for out
    while q.empty() == False:
        po, isIn = q.get()
        if isIn:
            # in
            markin[po] = 1
            inset.add(po)
            for i in range(0, n):
                if gm[po][i] == 1 and i == n - 1:
                    # if connect to END
                    outset.add(po)
                elif gm[po][i] == 1 and i != po and markout[i] == 0:
                    q.put((i, False))
                    markout[i] = 1
        else:
            # out
            markout[po] = 1
            outset.add(po)
            for i in range(0, n):
                if gm[i][po] == 1 and i == 0:
                    # if connected by SRC
                    inset.add(po)
                elif gm[i][po] == 1 and i != po and markin[i] == 0:
                    q.put((i, True))
                    markin[i] = 1
    # check if all in can go to all out
    fine = checkFine(gm, inset, outset)
    # if yes, return set
    if fine:
        nodes = inset | outset
        if len(nodes) < 2:
            return None
        return nodes
    else:
        return None

def checkFine(gm, inset, outset):
    nodes = inset | outset
    m = len(gm)
    gt = [[0 for i in range(m)] for j in range(m)]
    for k in nodes:
        for i in nodes:
            for j in nodes:
                if i == j or gm[i][j] == 1 \
                        or (gm[i][k] == 1 and gm[k][j] == 1):
                    gt[i][j] = 1
    for i in inset:
        for j in outset:
            if gt[i][j] == 0:
                return False
    return True

def debugOut(g):
    for x in g:
        print x
