#!/usr/bin/python27 -u

import sys
import tkFileDialog
import tkMessageBox

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
from WfmFromXML import *
from WfmFromProj import *
from SaveWfmToFile import *

from Soundness import *
from LocalOptCorrect import *
from ExtAndComb import *

class WfViewer(Frame):
    def __init__(self, master=None, width=1100, height=600):

        Frame.__init__(self, master, width=1100, height=600)
        self.grid(sticky=N+E+S+W)

        self.wfm = None
        self.view = None

        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        
        self.menu_bar = Menu(top, tearoff=0)
        top["menu"] = self.menu_bar
        self.__initFileMenu()
        self.__initViewMenu()
        self.__initAlgorithmsMenu()
        self.file_menu.add_command(label="Exit", command=top.quit)

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
        self.info_panel.insert(END, ("*ID", "%d" %act_id))
        d=dict()
        for key, val in self.wfm[1].items():
            if key[0]==act_id:
                d[key[1]]=val
        for keyval in d.items():
            self.info_panel.insert(END, keyval)

    def displayViewActInfo(self, act_id, act_list):
        self.info_panel.delete(0, END)
        self.info_panel.insert(END, ("*VID", "%d" %act_id))

        if act_list != None:
            for i in act_list:
                self.info_panel.insert(END, ("*id:%d" %i, ""))
                d = dict()
                for key, val in self.wfm[1].items():
                    if key[0] == i:
                        d[key[1]]=val
                for keyval in d.items():
                    self.info_panel.insert(END, keyval)
        
        self.model_canvas.highlightoff()
        self.model_canvas.highlight(act_list)

    def refreshWfm(self, wfm = None):
        if wfm == None:
            wfm = self.wfm
        self.wfm = None
        self.wfm_canvas.clear()
        self.wfm = wfm
        self.wfm_canvas.drawWf(self.wfm)

    def refreshView(self, view = None):
        if view == None:
            view = self.view
        self.view = None
        self.view_canvas.clear()
        self.view = view
        self.wfm = (self.wfm[0], self.wfm[1], self.wfm[2], self.view[3])
        self.view_canvas.drawWf(self.view)

    def removeInfo(self):
        self.info_panel.delete(0, END)

    def highlightoff(self):
        self.model_canvas.highlightoff()
        self.view_canvas.highlightoff()

    def __initFileMenu(self):
        # add FILE menu items
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.__openHandler)
        self.file_menu.add_command(label="Save as", command=self.__saveHandler)
        self.file_menu.add_command(label="Save view", command=self.__saveViewHandler)
        self.file_menu.add_separator()

    def __initViewMenu(self):
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

    def __initAlgorithmsMenu(self):
        # add ALGOR menu items
        self.algorithms_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Algorithms", menu=self.algorithms_menu)

        self.algorithms_menu.add_command(label="Check soundness", command=self.__checkSoundness)
        self.algorithms_menu.add_command(label="Weakly local-opt correct", command=self.__weakCorrect)
        self.algorithms_menu.add_command(label="Strong local-opt correct", command=self.__strongCorrect)
        self.algorithms_menu.add_command(label="Extend and combine", command=self.__extendAndComb)

    def __checkSoundness(self):
        if self.wfm == None:
            tkMessageBox.showerror('ERROR', 'No view is loaded')
            return
        if self.wfm[3] == None:
            tkMessageBox.showerror('ERROR', 'No view is loaded')
            return
        isSound, unsoundNodes = isViewSound(*(self.wfm))
        if isSound:
            prompt = "The view is SOUND"
            tkMessageBox.showinfo('Check view soundness', prompt)
        else:
            prompt = "The view is NOT SOUND"
            tkMessageBox.showinfo('Check view soundness', \
                "%s.\nUnsound view nodes are: %s" %(prompt,str(unsoundNodes)))
    
    def __weakCorrect(self):
        print "### weak correct"
        new_view = weakOptimalCorrect(self.wfm)
        self.refreshView(new_view)

    def __strongCorrect(self):
        pass #TODO

    def __extendAndComb(self):
        print "### extend and combine"
        new_view = extAndComb(self.wfm)
        self.refreshView(new_view)

    def __openHandler(self):
        filename = tkFileDialog.askopenfilename(defaultextension=".wfm",
                filetypes=[("workflow model file", "*.wfm | *.xml"), ("other", "*.*")])
        if filename == None or filename.strip() == "":
            return
        # clean up
        self.wfm = None
        self.view = None
        self.model_canvas.clear()
        self.view_canvas.clear()
        # add new 
        if filename[-4:].lower() == '.wfm':
            self.wfm = wfmObjectFromFile(filename)
        else:
            self.wfm = wfmObjectFromXML(filename)
        self.view = wfmObjectFromProj(self.wfm)
        self.model_canvas.drawWf(self.wfm)
        self.view_canvas.drawWf(self.view)

    def __saveHandler(self):
        if self.wfm == None:
            return
        filename = tkFileDialog.asksaveasfilename(defaultextension=".wfm", 
                filetypes=[("workflow model file", "*.wfm"), ("other", "*.*")])
        filename = filename.strip()
        if filename == None or filename == '':
            return
        wfmObjectToFile(filename, self.wfm)

    def __saveViewHandler(self):
        if self.wfm == None or self.wfm[3] == None:
            return
        filename = tkFileDialog.asksaveasfilename(defaultextension=".wfm", 
                filetypes=[("workflow model file", "*.wfm"), ("other", "*.*")])
        filename = filename.strip()
        if filename == None or filename == '':
            return
        wfmObjectToFile(filename, (self.view[0], None, True, None)) 
 
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
