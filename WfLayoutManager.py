import random
from WfActivity import *

class WfLayoutManager:
    def __init__(self, wfm=None, maxx=1280, maxy=1024,
            actwidth=10, actheight=10):
        self.maxx = maxx
        self.maxy = maxy
        self.activities = None
        self.dependencies = None

        WfActivity.width = actwidth
        WfActivity.height = actheight

        if wfm != None:
            self.setWfm(wfm)

    def setWfm(self, wfm):
        self.wfm = wfm
        self.activities = None
        self.dependencies = None
        try:
            self.generateLayout()
        except Exception, inst:
            print "## set layout failed."
            print str(inst)
            self.wfm = None

    def generateLayout(self):
        if self.wfm == None:
            return None
        if self.activities != None :
            return (self.activities, self.dependencies)
        
        self.activities = []
        for i in range(len(self.wfm[0])):
            randx = random.randint(1, self.maxx)
            randy = random.randint(1, self.maxy) #TODO
            self.activities += [WfActivity(randx, randy)]

        self.dependencies = []
        wfm = self.wfm
        if wfm[2]:
            for i in range(len(wfm[0])):
                for j in range(len(wfm[0])):
                    if wfm[0][i][j] == 1:
                        self.dependencies += [(self.activities[i], 
                            self.activities[j])]
        else :
            for i in range(len(wfm[0])):
                for j in range(len(wfm[0][i])):
                    self.dependencies += [(self.activities[i],
                        self.activities[wfm[0][i][j]])]

        return (self.activities, self.dependencies)

    def regenerateLayout(self):
        self.activities = None
        self.dependencies = None
        return self.generateLayout()
