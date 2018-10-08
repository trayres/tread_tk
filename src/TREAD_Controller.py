# GUI imports
import tkinter as tk
from tkinter import ttk, filedialog

from TREAD_Point import *
from TREAD_PopupMenu import *
from TREAD_View import *
from TREAD_Enums import *
from TREAD_StateMachine import *


class Controller(object):
    ################################################################################
    # Setup, Menus, Scrollbars, Bindings
    ################################################################################
    def __init__(self, master):
        self.master = master
        self.popup_menu = PopupMenu(self.master)
        self.view = View(master, self)  # Master is Root window, Controller is self
        self.system_state = SystemState.IDLE
        self.drag_data = {"x": 0, "y": 0, "item": None}
        self.x = 0
        self.y = 0
        self.state_machine = StateMachine(self, self.view.canvas)
        self.keys = set()
        self.scale = 1.0
        self.setup_menus()
        self.setup_bindings()
        self.last_mb1_item = {"time": None,
                              "canvas id": None}  # Then we need a "lookup statemachine object by canvas id" function. We also need a "Is state?" or "Is label?" function by ID, so we can tell what the user is clicking on.

        self.last_mb1_item_mk1 = None  # Wonder if we can get away with an even simpler implementation
        # We might actually need a concept of layers
        self._transition_pts = list()
        self._transition_line = list()

        self.dbg_edit_once = 0

    def setup_menus(self):
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)  # Says that root will get the menu

        self.mnu_file = tk.Menu(self.menu)
        self.mnu_file.add_command(label="Exit", command=self.master.destroy)
        self.menu.add_cascade(label="File", menu=self.mnu_file)

        self.mnu_debug = tk.Menu(self.menu)
        self.mnu_debug.add_command(label="Debug CMD 0", command=self.debug)
        self.menu.add_cascade(label="Debug", menu=self.mnu_debug)

    def setup_bindings(self):
        self.view.canvas.bind("<ButtonPress-1>", self.mouseB1)
        self.view.canvas.bind("<Double-Button-1>", self.mouseDblB1)
        self.view.canvas.bind("<KeyPress>", self.keypress)
        self.view.canvas.bind("<KeyRelease>", self.keyrelease)
        self.view.canvas.bind("<ButtonRelease-1>", self.mouseB1release)
        self.view.canvas.bind("<B1-Motion>", self.mouseB1motion)
        self.view.canvas.bind("<ButtonPress-3>", self.mouseB3)
        self.view.canvas.bind("<Motion>", self.mouseMove)

    # Events
    def mouseB1(self, event):
        # Setup Convenient Reference to Canvas
        c = self.view.canvas
        if self.system_state == SystemState.IDLE:
            pass
        elif self.system_state == SystemState.OBJECTS_SELECTED:
            pass
        elif self.system_state == SystemState.EDIT_OBJECT_PROPERTIES:
            pass
        elif self.system_state == SystemState.EDIT_CANVAS_TEXT:
            pass
        elif self.system_state == SystemState.ADD_TRANSITION_1:
            print("TRANSITION POINT 1")
            self._transition_pts.append((c.canvasx(event.x),c.canvasy(event.y)))
            self.temp_pt_1 = c.create_oval(c.canvasx(event.x) - 5, c.canvasy(event.y) - 5, c.canvasx(event.x) + 5,
                                                     c.canvasy(event.y) + 5, outline="black", fill="red",
                                                       tags=("temp_pt_1"))
            self.system_state = SystemState.ADD_TRANSITION_2

        elif self.system_state == SystemState.ADD_TRANSITION_2:
            # c.delete("temp_pt_1")
            print("TRANSITION POINT 2")
            self._transition_pts.append((c.canvasx(event.x), c.canvasy(event.y)))
            print("_transition_pts")
            print(self._transition_pts)
            # Draw a line for what we just added
            points = []
            points.append(self._transition_pts[0])
            points.append(self._transition_pts[1])
            self._transition_line.append(c.create_line(points, width=2, fill="black", tags =("temp_line_1")))
            self.system_state = SystemState.ADD_TRANSITION_3
        elif self.system_state == SystemState.ADD_TRANSITION_3:
            print("TRANSITION POINT 3")
            #c.delete("temp_line")
            #c.delete("temp_pt_2")
            self._transition_pts.append((c.canvasx(event.x), c.canvasy(event.y)))
            # Call the add_transition function with the points specified
            self.state_machine.addTransition(self._transition_pts)
            self.system_state = SystemState.IDLE
            self._transition_pts = list()
            

        print("MB1")
        print("System State:" + repr(self.system_state))
        closest_item = c.find_closest(c.canvasx(event.x), c.canvasy(event.y))
        print("Closest item:")
        print(closest_item)
        print("Closest item is a:")
        print(self.state_machine.canvas_id_type(closest_item))
        print("Above this")

        c.delete("highlight")

        #if self.state_machine.canvas_id_type(closest_item) == 'state' or 'transition':
        #    c.delete("highlight")

        if len(closest_item) > 0:
            self.last_mb1_item_mk1 = closest_item[0]
        print(closest_item)

    def mouseDblB1(self, event):
        c = self.view.canvas
        if c.type(tk.CURRENT) != "text":
            print("NOT A TEXT ITEM")
            return
        self.highlight(tk.CURRENT)
        self.system_state = SystemState.EDIT_CANVAS_TEXT

        closest_item = c.find_closest(c.canvasx(event.x), c.canvasy(event.y))
        if len(closest_item) > 0 and self.last_mb1_item_mk1 == closest_item[0]:
            print("Double tap on the same item!")

    def mouseB1release(self, event):
        print("rel mb1")

    def mouseMove(self, event):
        c = self.view.canvas
        self.x = c.canvasx(event.x)
        self.y = c.canvasy(event.y)
        if self.system_state == SystemState.IDLE:
            pass
        elif self.system_state == SystemState.OBJECTS_SELECTED:
            pass
        elif self.system_state == SystemState.EDIT_OBJECT_PROPERTIES:
            pass
        elif self.system_state == SystemState.EDIT_CANVAS_TEXT:
            pass
        elif self.system_state == SystemState.ADD_TRANSITION_1:
            c.delete("transition_indicator")
            self._temp_x = c.canvasx(event.x)
            self._temp_y = c.canvasy(event.y)
            self.transition_indicator = c.create_oval(c.canvasx(event.x) - 5, c.canvasy(event.y) - 5, c.canvasx(event.x) + 5,
                                                     c.canvasy(event.y) + 5, outline="black", fill="red",
                                                       tags=("transition_indicator"))
        # Delete and redraw the user's cursor
        elif self.system_state == SystemState.ADD_TRANSITION_2:
            c.delete("transition_indicator")
            c.delete("temp_pt_2")
            c.delete("temp_line")
        # Delete and redraw the user's cursor, the first point, and the temp line object
            self.temp_pt_2 = c.create_oval(c.canvasx(event.x) - 5, c.canvasy(event.y) - 5, c.canvasx(event.x) + 5,
                                                     c.canvasy(event.y) + 5, outline="black", fill="red",
                                                       tags=("temp_pt_2"))
            points = [(self._temp_x,self._temp_y),(c.canvasx(event.x),c.canvasx(event.y))]
            self.temp_line = c.create_line(points, width=2, fill="black", tags =("temp_line"))
        elif self.system_state == SystemState.ADD_TRANSITION_3:
            c.delete("temp_line")
            c.delete("temp_pt_3")
            self.temp_pt_3 = c.create_oval(c.canvasx(event.x) - 5, c.canvasy(event.y) - 5, c.canvasx(event.x) + 5,
                                                     c.canvasy(event.y) + 5, outline="black", fill="red",
                                                       tags=("temp_pt_3"))
            print("TRANSITION POINTS")
            print(self._transition_pts)
            print(self._transition_pts[1])
            points = [self._transition_pts[1],(c.canvasx(event.x),c.canvasx(event.y))]
            self.temp_line = c.create_line(points, width=2, fill="black", tags =("temp_line"))

    def mouseB1motion(self, event):
        print("MB1 Motion")
        c = self.view.canvas
        self.x = c.canvasx(event.x)
        self.y = c.canvasy(event.y)

    def mouseB3(self, event):
        # empty the menu
        self.popup_menu.clear_menu()
        # build the menu commands
        # Check to see if we're over an item - if we are, let's build the context sensitive part of the menu as well! TODO:

        command = [["debug", self.debug], ["debug0", self.debug0], ["Add State", self.addState],
                   ["Add Transition", self.addTransition]]
        self.popup_menu.build_menu(command)
        # Get the point to put the menu at
        aPoint = Point()
        aPoint.x, aPoint.y = self.master.winfo_pointerxy()
        # move it a bit for usability
        aPoint.x = aPoint.x + 40
        aPoint.y = aPoint.y + 8
        # Now popup the menu
        self.popup_menu.popup(aPoint)

    def keypress(self, event):
        c = self.view.canvas
        self.keys.add(event.char)
        self.keys.add(event.keysym)

        if event.keysym == 'Shift_L':
            print("LEFT SHIFT, BUDDY")

        if self.last_mb1_item_mk1 is not None:
            item_type = c.type(self.last_mb1_item_mk1)
        else:
            item_type = None
        if item_type != 'text':
            print("Selected canvas item is not text item")
            return
        _current_text = c.itemcget(self.last_mb1_item_mk1, 'text')

        print(event.keysym)
        if self.system_state == SystemState.EDIT_CANVAS_TEXT:
            print("We should be editing.")

            if event.char >= " ":
                print("Its a printable character...")
                # c.insert(item, "insert", event.char)
                _current_text = _current_text + event.char
                # update the item
                c.itemconfig(self.last_mb1_item_mk1, text=_current_text)
                self.highlight(self.last_mb1_item_mk1)
            elif event.keysym == "BackSpace":
                _current_text = _current_text[:-1]
                c.itemconfig(self.last_mb1_item_mk1, text=_current_text)
                self.highlight(self.last_mb1_item_mk1)
                # navigation
            elif event.keysym == "Home":
                pass
            elif event.keysym == "End":
                pass
            elif event.keysym == "Right":
                pass
            elif event.keysym == "Left":
                pass
            else:
                pass  # print event.keysym
        elif self.system_state == SystemState.IDLE:
            print("Cursor should be gone")

    def keyrelease(self, event):
        if event.char in self.keys:
            self.keys.remove(event.char)
        if event.keysym in self.keys:
            self.keys.remove(event.keysym)

    # State Commands
    def addState(self):
        print("Add a state")
        self.state_machine.addState(self.x, self.y, self.scale, StateType.NORMAL)

    def addTransition(self):
        print("START: Add a transition")
        c = self.view.canvas
        #self.state_machine.addTransition()
        self.system_state = SystemState.ADD_TRANSITION_1
        #Add a temporary red dot for the transition marker
        #Check the xy loc first to make sure it isn't a snap point
        

    # Canvas Editing
    def has_focus(self):
        c = self.view.canvas
        return c.focus()

    def highlight(self, item):
        # mark focused item.  note that this code recreates the
        # rectangle for each update, but that's fast enough for
        # this case.
        # TODO: We need to remove the dependence on c.focus(tk.CURRENT) and use stored state to do those operations, so that we can highlight properly if the mouse is moved after the text box is selected!
        c = self.view.canvas
        bbox = c.bbox(item)
        c.delete("highlight")
        if bbox:
            i = c.create_rectangle(
                bbox, fill="white",
                tag="highlight"
            )
            c.lower(i, item)
            # move focus to item
        c.focus_set()  # move focus to canvas

    # Testing using the canvas tags to do some lifting...
    def State_MB1(self,event):
        c = self.view.canvas
        print("STATEMODEL_MB1")

        self.drag_data["item"] = c.find_closest(c.canvasx(event.x), c.canvasy(event.y))[0]
        self.drag_data["x"] = c.canvasx(event.x)
        self.drag_data["y"] = c.canvasy(event.y)

    def State_MB1release(self,event):
        print("Statemodel_MB1Release")
        self.drag_data["item"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0

    def State_MB1Move(self,event):
        c = self.view.canvas
        print("STATEMODEL MB1MOVE")
        delta_x = c.canvasx(event.x) - self.drag_data["x"]
        delta_y = c.canvasy(event.y) - self.drag_data["y"]
        # move the object the appropriate amount
        c.move(self.drag_data["item"], delta_x, delta_y)
        print(self.state_machine.canvas_id_map)
        print("DRAG DATA ITEM")
        print(self.drag_data["item"])
        if self.state_machine.canvas_id_type(self.drag_data["item"]) == "state":
            # Get state's associated state_label
            c.move(self.drag_data["item"]+1,delta_x,delta_y) # TODO: DIRTY HACK
        # record the new position
        self.drag_data["x"] = c.canvasx(event.x)
        self.drag_data["y"] = c.canvasy(event.y)
        
    def StateLabel_MB1(self,event):
        pass
    def StateLabel_MB1release(self,event):
        pass
    def StateLabel_MB1Move(self,event):
        pass
        
    def StateLabel_DblMB1(self,event):
        pass


    # Debug Commands
    def debug(self):
        print("WHY THO")
        c = self.view.canvas
        print(c.focus())
        c.itemconfig(2, state="disabled")

    def debug0(self):
        print("SAME THO")
        c = self.view.canvas
        scaled_size = 50
        c.create_oval(self.x - scaled_size, self.y - scaled_size, self.x + scaled_size, self.y + scaled_size,
                      outline="black", fill="green", tags="state")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("ContextPopupMenu Test!")
    root.option_add('*Menu.tearOff', 0)
    w = 800
    h = 650
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.frame = tk.Frame(root, width=600, height=600)
    root.frame.pack()
    controller = Controller(root)  # Controller creates the View, the PopupMenu

    root.mainloop()
