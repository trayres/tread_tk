#GUI imports
import tkinter as tk
from tkinter import ttk, filedialog

class View(object): #Observer
    def __init__(self,master, controller):
        self.frame = tk.Frame(master, width = 600, height = 600)
        self.frame.pack(fill="both", expand=True)
        
        self.canvas = tk.Canvas(self.frame,width=600,height=600,scrollregion=(0,0,1600,1600))
        self.canvas.pack(fill="both", expand=True)
        
        self.hbar=ttk.Scrollbar(self.canvas,orient=tk.HORIZONTAL)
        self.hbar.config(command=self.canvas.xview)
        
        self.hbar.pack( side=tk.BOTTOM,fill=tk.X)
        
        
        self.vbar=ttk.Scrollbar(self.canvas,orient=tk.VERTICAL)
        self.vbar.pack(side=tk.RIGHT,fill=tk.Y)
        
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(xscrollcommand=self.hbar.set)
        self.canvas.config(yscrollcommand=self.vbar.set)
        
        
        self.sizegrip = ttk.Sizegrip(self.frame)
        self.sizegrip.pack(side=tk.BOTTOM, fill= tk.X)
        self.canvas.focus_force()
        

"""Test our View class in isolation"""        
if __name__ =="__main__":
    root = tk.Tk()
    root.title("tkTREAD")
    root.option_add('*Menu.tearOff',0)
    w = 800
    h = 650
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2)-(w/2)
    y = (hs/2)-(h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    view = View(root, None)
    #AController.setup_RightClickContextPopupMenu()
    #AController.AView.do_bindings()
    root.mainloop()
