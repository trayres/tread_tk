#GUI imports
import tkinter as tk
from tkinter import ttk, filedialog


from TREAD_Enums import *

class StateModel(object):    
    
    def __init__(self,name,canvas,x,y,canvas_id_map, scale = 1.0, state_type = StateType.NORMAL, size = 50,):
        self.name = name
        self.canvas = canvas
        self.x = x
        self.y = y
        scaled_size = scale * size
        self.drawn_state = self.canvas.create_oval(x - scaled_size, y-scaled_size,x+scaled_size,y+scaled_size,outline = "black",fill = "green", tags = ("state",name+"_state"))
        self.drawn_label = self.canvas.create_text(x,y,fill="darkblue",font="Times 12",text=name,tags = ("state_label",name+"_label"), state = 'normal')
        canvas_id_map[self.drawn_state] = "state"
        canvas_id_map[self.drawn_label] = "state_label"
        print("Drawn_state is:")
        print(self.drawn_state)
        print("drawn_label is:")
        print(self.drawn_label)
        self.canvas.focus_force()
        self.x = x
        self.y = y
        self.state_type = state_type
        self.size = size
        #self.bbox = BoundingBox(x-size,y-size,x+size,y+size,self.canvas) #Because of screen coordinates

        #We need something to switch between the two modes, one of which we draw the label (drawn_label) the other of which allows us to easily grab text (entry_label).
        self.drawn_or_entry_label = DrawnOrEntry.DRAWN
        #Actually this got handled by itemconfig in the controller. Huh.

    def setName(self,name):
        self.name = name

    def draw_bbox(self):
        #self.bbox.draw_bbox()
        pass
        #use tk's bbox on the canvas items for this

    def move_all(self,x,y):
        pass
    
    def move_label(self,x,y): #remember to move the entrylabel as well
        pass

    def switch_label(self):
        if drawn_or_entry_label == DrawnOrEntry.DRAWN:
            drawn_or_entry_label = DrawnOrEntry.ENTRY
        elif drawn_or_entry_label == DrawnOrEntry.ENTRY:
            drawn_or_entry_label = DrawnOrEntry.DRAWN
        else:
            print("Error in switching labels.") #Should only be 2 options
            
class TransitionModel(object):
    def __init__(self,name,canvas,points = None):
        self.name = name
        self.canvas = canvas
        self.points = points
        self.drawn_transition = self.canvas.create_line(self.points, width=2, fill="yellow", smooth=True)

    def setTransitionName(self, name):
        self.name = name

    def setStartState(self,state):
        self.startState = state

    def setStopState(self,state):
        self.stopState = state

    def setPriority(self,priority):
        self.priority = priority            

"""Takes StateMdoels and TransitionModels (states and transitions), and uses them
   to build a machine. It can also do operations on those statemodels and transition
   models"""
class StateMachine(object):
    transitionList = {}
    stateList = {}
    transitionList = {}
    
    stateMachineName = "TREAD_machine" #Make this a configurable parameter that we can load from a configuration file
    
    def __init__(self, controller, canvas, stateList = None):
        self.controller = controller
        self.canvas = canvas
        self.selected = set()
        self.canvas_id_map = {}

    def addState(self, x, y, scale, state_type):
        newStateName = StateMachine.generate_next_default_state_name()
        newState = StateModel(newStateName,self.canvas,x,y,self.canvas_id_map, scale, state_type ) #canvas_id_map TODO
        print("newStateName:"+newStateName+" x:"+str(x)+" y:"+str(y))
        #newState.setName(newStateName)
        self.stateList[newStateName] = newState
        self.canvas.tag_bind("state",'<ButtonPress-1>',self.controller.State_MB1)
        self.canvas.tag_bind("state", "<ButtonRelease-1>", self.controller.State_MB1release)
        self.canvas.tag_bind("state", "<B1-Motion>", self.controller.State_MB1Move)
    
    def addTransition(self,points): #3 points for a transition, not 1
        newTransitionName = StateMachine.generate_next_default_transition_name
        newTransition = TransitionModel(newTransitionName,self.canvas,points)

    def addSelected(self, anObject):
        self.selected.add(anObject)

    def removeSelected(self,anObject):
        self.selected.remove(anObject)

    def draw_bbox(self):
        for state in self.stateList:
            self.stateList[state].draw_bbox() #stateList[state] returns a StateModel object

    def print_all_states(self):
        print(self.stateList)

    def find_states_in_loc(self,x,y):
        #Check all the bounding boxes for each state, to see if the point is in them.
        states_here = []
        for state in self.stateList:
            aState = self.stateList[state]
            aPoint = Point(x,y)
            if aState.bbox.hit_test(aPoint):
                print("Inside a state!")
                states_here.append(state)
                
        print("states here:")
        print(states_here)
        print(type(states_here))
        return states_here
            
    def find_selected_states_in_loc(self,x,y):
        #similar to the above, but we only check already selected states
        pass
        
    def canvas_id_type(self, id):
        print("ID IS:")
        print(id)
        print("self.canvas_id_map is:")
        print(self.canvas_id_map)
        return self.canvas_id_map.get(id)
        
    @classmethod
    def generate_next_default_state_name(cls):
        stateName = 'S'
        idx = 0
        #print(stateName + str(idx))
        while  stateName + str(idx)  in cls.stateList:
            idx = idx + 1
        return stateName + str(idx)
        
    @classmethod
    def generate_next_default_transition_name(cls):
        transitionName = 'transition'
        
    #Load from file, save to file?