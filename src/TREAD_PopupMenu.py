#GUI imports
import tkinter as tk
from tkinter import ttk, filedialog

from TREAD_Point import *

#import unittest

class _PopupMenu_Test(object):
    def __init__(self, master):
        self.master = master
        
        self.test_tuple = ( ("callback 0 text",self.callback0),
                          ("callback 1 text",self.callback1))
    def callback0(self):
        print("Callback 0!")
    
    def callback1(self):
        print("Callback 1")
        
    def mouseB1(self,event):
        #Create a point object
        aPoint = Point(event.x_root,event.y_root)
        print(event.x_root)
        print(event.y_root)
        #Call it
        
        aContextPopupMenu = PopupMenu(self.master)
        aContextPopupMenu.build_menu(self.test_tuple)
        
        #self.master, self.test_tuple,aPoint)
        aContextPopupMenu.popup(aPoint)
        

"""A context popup menu class that takes a master element and a tuple of 2-element tuple(s) of the form (text, callback). Example:
(("Command Text 0", callback0),
 ("Command Text 1", callback1),
 ("Command Text 2", callback2))"""

class PopupMenu(object):
    def __init__(self,master):
        self.aMenu = tk.Menu(master)
        

    def build_menu(self,command_tuple):
        for command in command_tuple:
            self.aMenu.add_command(label=command[0], command = command[1])
        
    def clear_menu(self):
        last = self.aMenu.index("end")
        self.aMenu.delete(0,last)
        
        
    def popup(self,aPoint):
        try:  
            self.aMenu.tk_popup(aPoint.x,aPoint.y,0)
        finally:
            self.aMenu.grab_release()
            
if __name__ =="__main__":
    root = tk.Tk()
    root.title("ContextPopupMenu Test!")
    root.option_add('*Menu.tearOff',0)
    w = 800
    h = 650
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2)-(w/2)
    y = (hs/2)-(h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.frame = tk.Frame(root, width = 600, height = 600)
    root.frame.pack()
    a_PopupMenu_Test = _PopupMenu_Test(root)
                   
    root.frame.bind("<ButtonPress-1>",a_PopupMenu_Test.mouseB1)
    
    
    root.mainloop()
