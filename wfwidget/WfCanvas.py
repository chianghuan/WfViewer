from Tkinter import *
from WfActivity import *

class WfCanvas(Frame):
    def __init__(self, master=None, width=1500, height=1024,
            maxx=1500, maxy=1024):
        """Initialize the WfCanvas object.

        with width and height(painting region).
        """
        Frame.__init__(self, master)

        self.width = width
        self.height = height
        self.maxx = maxx
        self.maxy = maxy

        self.setActivitySize()
        self.setLineSize()

        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

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

        self.__movingActivity = None
        self.canvas.bind("<Button-1>", self.__mouseDownHandler)
        self.canvas.bind("<ButtonRelease-1>", self.__mouseUpHandler)

    def setActivitySize(self, width=10, height=10):
        WfActivity.width = width
        WfActivity.height = height

    def setLineSize(self, sz=3):
        self.linesz=sz

    def drawWf(self, activities, dependencies):
        """Draw the wf model."""
        self.__acts = {} 
        self.__depen = []
        for act in activities:
            a = self.drawActivity(act)
            self.__acts[a] = act
        for depen in dependencies:
            d = self.drawDependency(depen[0], depen[1])
            self.__depen.append([d, depen[0], depen[1]])

        # for test only
        # self.moveActivity(self.__acts.keys()[3], 0, 0)

    def drawGrid(self, gridx, gridy):
        """Draw the cavas background grid."""
        count = 0
        for x in range(0, self.maxx, gridx): 
            count += 1
            self.canvas.create_line(
                    x, 0,
                    x, self.maxy)
            for y in range(0, self.maxy, gridy):
                self.canvas.create_line(
                        x, y+(count%2)*gridy/2,
                        x+gridx, y+(count%2)*gridy/2)

    def drawActivity(self, activity):
        return self.canvas.create_rectangle(
                activity.x, activity.y,
                activity.x+WfActivity.width,
                activity.y+WfActivity.height,
                fill="grey")

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

    def moveActivity(self, aid, tx, ty):
        a = None
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
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        res = self.canvas.find_overlapping(x, y, x, y)
        if len(res) != 0:
            self.__movingActivity = res[0]
        else:
            self.__movingActivity = None

    def __mouseUpHandler(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        if self.__movingActivity != None and \
        self.__movingActivity in self.__acts.keys():
            self.moveActivity(self.__movingActivity, x, y)
