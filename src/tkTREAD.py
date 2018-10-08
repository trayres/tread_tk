#GUI imports
import tkinter as tk
from tkinter import ttk, filedialog
#State diagram representation using Graphviz
from graphviz import Digraph

from TREAD_Controller import *



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
    controller = Controller(root)
    root.mainloop()
