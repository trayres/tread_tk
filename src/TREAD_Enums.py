from enum import Enum

"""StateType determines what types of state is on the machine diagram"""
class StateType(Enum):
    RESET = 1
    NORMAL = 2
    DELAY = 3
    HIERARCHICAL = 4

class SystemState(Enum):
    IDLE = 1
    OBJECTS_SELECTED = 2
    EDIT_OBJECT_PROPERTIES = 3
    EDIT_CANVAS_TEXT = 4
    ADD_TRANSITION_1 = 5
    ADD_TRANSITION_2 = 6
    ADD_TRANSITION_3 = 7
    
class DrawnOrEntry(Enum):
    DRAWN = 1
    ENTRY = 2
