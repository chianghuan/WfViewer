#!/usr/bin/python27

import sys
import tkFileDialog

from Tkinter import *

sys.path.append("./wfwidget")
sys.path.append("./wfm")
sys.path.append("./algor")

from WfCanvas import *
from WfActivity import *
from WfLayoutManager import *
from WfMultiListbox import *

from WfElasticLayout import *
from WfmFromFile import *
from WfmFromProj import *

class WfViewer(Frame):
    def __init__(self, master=None, width=1100, height=600):

        Frame.__init__(self, master, width=1100, height=600)
        self.grid(sticky=N+E+S+W)

        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        
        self.menu_bar = Menu(top, tearoff=0)
        top["menu"] = self.menu_bar

        # add FILE menu items
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.__openHandler)
        self.file_menu.add_command(label="Save as", command=self.__saveHandler)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=top.quit)

        # add VIEW menu items
        self.__view_cb = IntVar()
        self.__split_cb = StringVar(value="VER")
        self.view_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_checkbutton(label="Show workflow view", 
                variable=self.__view_cb, onvalue=1, offvalue=0, command=self.__viewOnHandler)
        self.view_menu.add_radiobutton(label="Split vertically",
                variable=self.__split_cb, value="VER", command=self.__splitHandler)
        self.view_menu.add_radiobutton(label="Split horizontally",
                variable=self.__split_cb, value="HOR", command=self.__splitHandler)

        # Layout 
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1, minsize=30)
        self.columnconfigure(1, weight=4, minsize=500)
        self.columnconfigure(2, weight=4)

        # Create main widgets
        self.info_panel = WfMultiListbox(self, (('Attribute', 12), ('Value', 20)))
        self.info_panel.grid(row=0, column=0, rowspan=2, sticky=N+S+E+W)

        self.model_canvas = WfCanvas(self)
        self.model_canvas.grid(row=0, column=1, sticky=N+S+E+W)

        layoutMan = WfElasticLayout(maxx=1280, maxy=768,
                actwidth=20, actheight=20)
        self.model_canvas.setLayout(layoutMan)

        self.view_canvas = WfCanvas(self, ctype="VIEW")
        layoutView = WfElasticLayout(maxx=1280, maxy=768,
                actwidth=20, actheight=20)
        self.view_canvas.setLayout(layoutView)
        self.view_canvas.grid_remove()

    def displayInfo(self, act_id):
        self.info_panel.delete(0, END)
        self.info_panel.insert(END, ("ID", "%d" %act_id))
        d=dict()
        for key, val in self.wfm[1].items():
            if key[0]==act_id:
                d[key[1]]=val
        for keyval in d.items():
            self.info_panel.insert(END, keyval)

    def displayViewActInfo(self, act_id, act_list):
        self.info_panel.delete(0, END)
        self.info_panel.insert(END, ("VID", "%d" %act_id))

        # TODO set info
        
        self.model_canvas.highlightoff()
        self.model_canvas.highlight(act_list)

    def removeInfo(self):
        self.info_panel.delete(0, END)

    def highlightoff(self):
        self.model_canvas.highlightoff()
        self.view_canvas.highlightoff()

    def __openHandler(self):
        filename = tkFileDialog.askopenfilename(defaultextension=".wfm",
                filetypes=[("workflow model file", "*.wfm"), ("other", "*.*")])
        if filename == None or filename.strip() == "":
            return
        # clean up
        self.wfm = None
        self.view = None
        self.model_canvas.clear()
        self.view_canvas.clear()
        # add new 
        self.wfm = wfmObjectFromFile(filename)
        self.view = wfmObjectFromProj(self.wfm)
        self.model_canvas.drawWf(self.wfm)
        self.view_canvas.drawWf(self.view)

    def __saveHandler(self):
        filename = tkFileDialog.asksaveasfilename(defaultextension=".wfm", 
                filetypes=[("workflow model file", "*.wfm"), ("other", "*.*")])
        if filename == None or filename.strip() == '':
            return
        pass #TODO 

    def __viewOnHandler(self):
        if self.__view_cb.get() == 1:
            if self.__split_cb.get() == "VER":
                self.view_canvas.grid(row=0, column=2, sticky=N+S+E+W)
            elif self.__split_cb.get() == "HOR":
                self.view_canvas.grid(row=1, column=1, sticky=N+S+E+W)
        else:
            self.view_canvas.grid_remove()

    def __splitHandler(self):
        if self.__split_cb.get() == "HOR" and self.__view_cb.get() == 1:
            self.view_canvas.grid_remove()
            self.view_canvas.grid(row=1, column=1, sticky=N+S+E+W)
        elif self.__split_cb.get() == "VER" and self.__view_cb.get() == 1:
            self.view_canvas.grid_remove()
            self.view_canvas.grid(row=0, column=2, sticky=N+S+E+W)


if __name__=="__main__":
    root = Tk()
    app = WfViewer(root)
    root.mainloop()
