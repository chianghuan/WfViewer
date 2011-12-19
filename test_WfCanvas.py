#!/usr/bin/python27

from Tkinter import *

from WfCanvas import *
from WfActivity import *
from WfLayoutManager import *

from WfmFromFile import *

if (__name__ == "__main__"):
    app = WfCanvas()
    app.master.tittle="Test WfCanvas"

    wfm = wfmObjectFromFile("sample.wfm")
    layoutMan = WfLayoutManager(wfm, maxx=800, maxy=600,
            actwidth=20, actheight=20)
        
    app.drawGrid(50, 80)
    app.drawWf(layoutMan.activities, layoutMan.dependencies)
    
    app.mainloop()
