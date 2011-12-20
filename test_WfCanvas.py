#!/usr/bin/python27

from Tkinter import *
import sys

sys.path.append("./wfwidget")
sys.path.append("./wfm")

from WfCanvas import *
from WfActivity import *
from WfLayoutManager import *

from WfElasticLayout import *

from WfmFromFile import *

import sys

if __name__ == "__main__":
    app = WfCanvas()
    app.master.tittle="Test WfCanvas"

    wfm = wfmObjectFromFile("wfm/sample.wfm")
    layoutMan = WfElasticLayout(maxx=1280, maxy=768,
            actwidth=20, actheight=20)
    app.setLayout(layoutMan)
        
    app.drawWf(wfm)
    
    app.mainloop()
