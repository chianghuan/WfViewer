from Tkinter import *
from WfActivity import *
from WfLayoutManager import *

class WfCanvas(Canvas):
    def __init__(self, master=None, width=1024, height=768,
            maxx=1500, maxy=1024, layout = None, wfm=None, ctype="MODEL"):
        """Initialize the WfCanvas object.

        with width and height(painting region).
        """
        self.master=master
        self.__type=ctype
        Canvas.__init__(self, master)

        self.__layoutManager = layout
        self.__wfm = wfm

        self.width = width
        self.height = height
        self.maxx = maxx
        self.maxy = maxy

        self.setActivitySize()
        self.setLineSize()

        self.grid(sticky=N+E+S+W)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, minsize=15)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, minsize=15)

        self.canvas = Canvas(self, 
                width=self.width, 
                height=self.height,
                scrollregion=(0, 0, maxx, maxy))
        self.canvas.grid(sticky=N+E+S+W, row=0, column=0)

        self.vScrollbar = Scrollbar(self, orient=VERTICAL,
                command=self.canvas.yview)
        self.vScrollbar.grid(row=0, column=1, sticky=N+S)

        self.hScrollbar = Scrollbar(self, orient=HORIZONTAL,
                command=self.canvas.xview)
        self.hScrollbar.grid(row=1, column=0, sticky=W+E)

        self.canvas["yscrollcommand"] = self.vScrollbar.set
        self.canvas["xscrollcommand"] = self.hScrollbar.set

        self.canvas["bg"] = "white"

        self.__last_res = -1
        self.__movingActivity = None
        self.canvas.bind("<Button-1>", self.__mouseDownHandler)
        self.canvas.bind("<ButtonRelease-1>", self.__mouseUpHandler)

    def setWfm(wfm):
        self.__wfm = wfm
        self.__layoutManager.setWfm(self.__wfm)

    def setActivitySize(self, width=10, height=10):
        WfActivity.width = width
        WfActivity.height = height

    def setLineSize(self, sz=1):
        self.linesz=sz

    def setLayout(self, layout):
        self.__layoutManager = layout

    def drawWf(self, wfm=None):
        """Draw the wf model."""
        if wfm != None:
            self.__wfm = wfm
        else:
            return

        if self.__layoutManager == None:
            print "## no layout specified"
            self.__layoutManager = WfLayoutManager(
                    maxx=self.maxx, maxy=self.maxy)
        self.__layoutManager.setWfm(self.__wfm)

        activities = self.__layoutManager.activities
        dependencies = self.__layoutManager.dependencies

        self.__acts = {} 
        self.__depen = []
        if activities != None:
            for act in activities:
                a = self.drawActivity(act)
#                print "act id: ", a
                self.__acts[a] = act
        if dependencies != None:
            for depen in dependencies:
                d = self.drawDependency(depen[0], depen[1])
                self.__depen.append([d, depen[0], depen[1]])

    def drawGrid(self, gridx, gridy):
        """Draw the cavas background grid."""
        count = 0
        for x in range(0, self.maxx, gridx): 
            count += 1
            self.canvas.create_line(
                    x, 0,
                    x, self.maxy,
                    tags="GRID")
            for y in range(0, self.maxy, gridy):
                self.canvas.create_line(
                        x, y+(count%2)*gridy/2,
                        x+gridx, y+(count%2)*gridy/2,
                        tags="GRID")

    def drawActivity(self, activity):
        objid = self.canvas.create_rectangle(
                activity.x, activity.y,
                activity.x+WfActivity.width,
                activity.y+WfActivity.height,
                fill=activity.color,
                tags=["ACT","aid=%d" %activity.aid])
        return objid

    def drawDependency(self, fromAct, toAct):
        ret = None
        if abs(fromAct.x-toAct.x) < abs(fromAct.y-toAct.y) :
            if toAct.y+WfActivity.height < fromAct.y :
                ret = self.canvas.create_line(
                        fromAct.getN()[0], fromAct.getN()[1],
                        toAct.getS()[0], toAct.getS()[1],
                        arrow=LAST, width=self.linesz)
            elif toAct.y > fromAct.y+WfActivity.height : 
                ret = self.canvas.create_line(
                        fromAct.getS()[0], fromAct.getS()[1],
                        toAct.getN()[0], toAct.getN()[1],
                        arrow=LAST, width=self.linesz)
        elif toAct.x < fromAct.x :
            ret = self.canvas.create_line(
                    fromAct.getW()[0], fromAct.getW()[1],
                    toAct.getE()[0], toAct.getE()[1],
                    arrow=LAST, width=self.linesz)
        else:
            ret = self.canvas.create_line(
                fromAct.getE()[0], fromAct.getE()[1],
                toAct.getW()[0], toAct.getW()[1],
                arrow=LAST, width=self.linesz)
        return ret

    def highlight(self, act_list):
        for aid in act_list:
            a = self.canvas.find_withtag("aid=%d" %aid)
            self.canvas.itemconfigure(a[0], fill="yellow")
            self.canvas.addtag_withtag("HL", "aid=%d" %aid)

    def highlightoff(self):
        for a in self.canvas.find_withtag("HL"):
#            print a
            self.canvas.itemconfigure(a, fill="grey")
        self.canvas.dtag("HL", "HL")
#        for a in self.canvas.find_withtag("HL"):
#            print "##### still have", a

    def moveActivity(self, aid, tx, ty):
        a = None
        if tx > self.maxx:
            tx = self.maxx - 100
        if ty > self.maxy:
            ty = self.maxy - 100
        if tx < 0:
            tx = 0
        if ty < 0:
            ty = 0
        if aid in self.__acts.keys():
            a = self.__acts[aid]
            dx = tx - a.x
            dy = ty - a.y
            a.setPosition(tx, ty)
            self.canvas.move(aid, dx, dy)

            for dep in self.__depen:
                if (dep[1] == a or dep[2] == a):
                    self.canvas.delete(dep[0])
                    dep[0]=self.drawDependency(dep[1], dep[2])

    def __mouseDownHandler(self, event):
        if self.__type=="MODEL":
            self.__modelMouseDownHandler(event)
        else:
            self.__viewMouseDownHandler(event)

    def __modelMouseDownHandler(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.__last_action_x = x
        self.__last_action_y = y
#        if self.__last_res != -1:
#            self.canvas.itemconfigure(self.__last_res, fill="grey")
        res = self.canvas.find_overlapping(x, y, x, y)
        if len(res) != 0 and ("ACT" in self.canvas.gettags(res[0])):
#            print res[0]  #DEBUG
#            print self.__acts[res[0]].aid
            self.__last_res = res[0]
#            self.canvas.itemconfigure(res[0], fill="yellow")
#            self.highlight([self.__acts[res[0]].aid])
            self.master.displayInfo(self.__acts[res[0]].aid)
            self.__movingActivity = res[0]
        else:
            self.__movingActivity = None
            self.master.removeInfo()

    def __viewMouseDownHandler(self, event):
        self.master.highlightoff()
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.__last_action_x = x
        self.__last_action_y = y
        if self.__last_res != -1:
            self.canvas.itemconfigure(self.__last_res, fill="grey")
        res = self.canvas.find_overlapping(x, y, x, y)
        if len(res) != 0 and ("ACT" in self.canvas.gettags(res[0])):
            self.__last_res = res[0]
            self.canvas.itemconfigure(res[0], fill="yellow")
            aid = self.__acts[res[0]].aid
#            print "###", aid
#            print "###", self.__wfm[3][aid]
            self.master.displayViewActInfo(aid,
                    self.__wfm[3][aid])
            self.__movingActivity = res[0]
        else:
            self.__movingActivity = None
            self.master.removeInfo()

    def __mouseUpHandler(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        if self.__movingActivity != None and \
        self.__movingActivity in self.__acts.keys() and \
        ( abs(self.__last_action_x - x) > 5 or abs(self.__last_action_y - y) > 5 ):
            self.moveActivity(self.__movingActivity, x, y)
            self.__last_action_x = x
            self.__last_action_y = y

    def clear(self):
        self.__wfm = None
        self.__acts = {} 
        self.__depen = []
        for i in self.canvas.find_all():
            self.canvas.delete(i)
