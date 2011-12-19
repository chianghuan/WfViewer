from WfLayoutManager import *

class WfElasticLayout(WfLayoutManager):
    """ A layout using simple elastic node method.
    
        ref to: http://doc.qt.nokia.com/4.7/graphicsview-elasticnodes.html
    """
    #TODO have to make the magic varies according to (maxx, maxy) 
    def __init__(self, wfm=None, maxx=1280, maxy=1024,
            actwidth=10, actheight=10):
        WfLayoutManager.__init__(self, wfm, maxx, maxy,
                actwidth, actheight)
        self.__convergency = 50

    def generateLayout(self):
        WfLayoutManager.generateLayout(self)
        for i in range(self.__convergency):
            if False == self.__converge():
                return

    def __converge(self):
        morefix = False 
        for act in self.activities:
            vx = 0.0
            vy = 0.0
            """calc push power"""
            for tac in self.activities:
                dx = act.x - tac.x
                dy = act.y - tac.y
                l = (dx*dx+dy*dy)*2 # It's a magic!
                if l>0 :
                    vx += dx*150/l
                    vy += dy*150/l # another magic!
            
            weight = (len(self.dependencies)+1)*10 # magic again!
            """calc pull power"""
            for dep in self.dependencies:
                if dep[0] == act or dep[1] == act:
                    dx = act.x - tac.x
                    dy = act.y - tac.y
                    vx -= dx/weight
                    vy -= dy/weight

            act.x += vx
            act.y += vy
            if abs(vx)>=1 or abs(vy)>=1:
                morefix = True 
        return morefix
