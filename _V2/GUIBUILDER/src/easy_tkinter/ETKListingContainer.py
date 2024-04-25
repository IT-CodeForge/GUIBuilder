from typing import Any, Iterable
from .ETKNoTKEventBase import ETKNoTKEventBase
from .ETKBaseObject import BaseEvents, ETKBaseObject
from .ETKBaseWidget import ETKBaseWidget
from .vector2d     import vector2d
from math         import pi
from enum         import Enum, auto
from .ObservableTypes import ObservableList
from .ETKContainer  import Alignments, ETKContainer

class ListingTypes(Enum):
    TOP_TO_BOTTOM = auto()
    BOTTOM_TO_TOP = auto()
    LEFT_TO_RIGHT = auto()
    RIGHT_TO_LEFT = auto()

class ETKListingContainer(ETKNoTKEventBase):
    def __init__(self, gui_object=None, offset:int = 10, alignment:Alignments=Alignments.MIDDLE_LEFT, listing_type:ListingTypes=ListingTypes.TOP_TO_BOTTOM):
        super().__init__()
        self.__my_alignment = alignment
        self.__alignment_type = vector2d(float(alignment.value[1]), float(alignment.value[0]))
        self.__listing_type = listing_type
        self.__offset = offset
        self.__elements = []
        self.__visibility = True
        self.__mov_flag = False 
        if gui_object == None:
            self.__my_pos = vector2d()
            self.__dimensions = vector2d()
            self.width = None
            self.height = None
        else:
            self.__my_pos = gui_object.pos
            self.__dimensions = vector2d(gui_object.width, gui_object.height)
    
    ######
    ###properties###
    ######
    @property
    def abs_pos(self)->vector2d:
        return self.__my_pos

    @property
    def pos(self)->vector2d:
        if self.parent != None:
            return self._parent._get_pos_in_parent(self)
        return self.__my_pos
    
    @pos.setter
    def pos(self, value:vector2d):
        if self.parent != None and not self._parent._validate("move", self):
            return
        my_pos = self.__my_pos
        self.__my_pos = value
        if my_pos != value:
            self._eventhandler(BaseEvents.CONFIGURED)
        self.__place_elements()
        if self.parent != None and self._parent._validate("move", self):
            self._parent._element_changed(self)
    
    @property
    def width(self)->int:
        if self.__dimensions.x == -1:
            return max([e[0].pos.x + e[0].width for e in self.__elements])
        return self.__dimensions.x
    
    @width.setter
    def width(self, value:int):
        if self.parent != None and not self._parent._validate("width", self):
            return
        if type(value) == int and value < 0:
            raise ValueError("objects must have a positive width")
        if value == None:
            value = -1
        my_width = self.__dimensions.x
        self.__dimensions.x = value
        if my_width != value:
            self._eventhandler(BaseEvents.CONFIGURED)
        self.__place_elements()
        if self.parent != None:
            self._parent._element_changed(self)
    
    @property
    def height(self)->int:
        if self.__dimensions.y == -1:
            return max([e[0].pos.y + e[0].height for e in self.__elements])
        return self.__dimensions.y
    
    @height.setter
    def height(self, value:int):
        if self.parent != None and not self._parent._validate("height", self):
            return
        if type(value) == int and value < 0:
            raise ValueError("objects must have a positive height")
        if value == None:
            value = -1
        my_height = self.__dimensions.y
        self.__dimensions.y = value
        if my_height != value:
            self._eventhandler(BaseEvents.CONFIGURED)
        self.__place_elements()
        if self.parent != None:
            self._parent._element_changed(self)
    
    @property
    def visible(self)->bool:
        return self.__visibility
    
    @visible.setter
    def visible(self, value):
        if self.parent != None and not self._parent._validate("visible", self):
            self.__visibility = value
            return
        visibilities = []
        for e in self.__elements:
            visibilities.append(e.visible)
            e.visible = False
        self.__visibility = value
        for index,e in enumerate(self.__elements):
            e.visible = visibilities[index]
        self._eventhandler("<Visible>")

    @property
    def alignment(self)->Alignments:
        return self.__my_alignment
    
    @alignment.setter
    def alignment(self, value:Alignments):
        self.__my_alignment = value
        self.__alignment_type = vector2d(float(value.value[0]),float(value.value[1]))
        self.__place_elements()
    
    @property
    def listing_type(self)->ListingTypes:
        return self.__listing_type
    
    @listing_type.setter
    def listing_type(self, value:ListingTypes):
        self.listing_type = value
        self.__place_elements()
    
    @property
    def offset(self)->int:
        return self.__offset
    
    @offset.setter
    def offset(self, value:int):
        self.__offset = value
        self.__place_elements()
    
    @property
    def elements(self)->ObservableList:
        return ObservableList(self.__ev_elements_changed, self.__elements)
    
    @elements.setter
    def elements(self, value:list):
        if type(value) != list:
            raise TypeError(f'"elements" of TGContainer can only be assigned a list and not {type(value)}')
        self.__ev_elements_changed(value)
    ######
    ######
    ######

    ######
    ###utils###
    ######
    def __vector_sum(self, iterable:Iterable)->vector2d:
        ret_val = vector2d()
        for elment in iterable:
            ret_val += elment
        return ret_val 
    ######
    ######
    ######

    ######
    ###calculate child positions###
    ######
    def __place_elements(self):
        if len(self.__elements) == 0:
            return
        
        if self.__listing_type in {ListingTypes.TOP_TO_BOTTOM, ListingTypes.BOTTOM_TO_TOP}:
            t_mode = int(self.alignment.value[0])
            t_sum = sum([e.height for e in self.__elements])
            t_ori = self.abs_pos.y
        else:
            t_mode = int(self.alignment.value[1])
            t_sum = sum([e.width for e in self.__elements])
            t_ori = self.abs_pos.x

        t_akt_max = 0
        match t_mode:
            case 0:
                t_akt_max = t_ori
            case 2:
                t_akt_max = t_ori + (self.height - t_sum)
            case 1:
                if self.__listing_type in {ListingTypes.TOP_TO_BOTTOM, ListingTypes.BOTTOM_TO_TOP}:
                    t_akt_max = t_ori + (self.height - t_sum) / 2
                else:
                    t_akt_max = t_ori + (self.width - t_sum) / 2

        for e in self.__elements:
            if self.__listing_type in {ListingTypes.TOP_TO_BOTTOM, ListingTypes.BOTTOM_TO_TOP}:
                cord_x = self.__calculate_1(int(self.alignment.value[1]), e.width, self.abs_pos.x, self.width)
                cord_y = t_akt_max
                t_akt_max = t_akt_max + e.height
            else:
                cord_y = self.__calculate_1(int(self.alignment.value[0]), e.height, self.abs_pos.y, self.height)
                cord_x = t_akt_max
                t_akt_max = t_akt_max + e.width

            
            
            self.__mov_flag = True
            e.pos = vector2d(cord_x, cord_y)

            print(self.name, getattr(e, "name", None), (cord_x, cord_y), e.pos)

            x = None
        

    def __calculate_1(self, mode, element_size, container_pos, container_size): # CHECK IF OUTSIDE CONTAINER
        match mode:
            case 0:
                return container_pos
            case 2:
                return container_pos + container_size - element_size
            case 1:
                return container_pos + (container_size - element_size) / 2


    
    ######
    ######
    ######
    
    ######
    ###Events###
    ######
    def __ev_elements_changed(self, my_list):
        element: ETKBaseWidget
        for element in [e for e in my_list if e not in self.__elements]:
            element.add_event("<Detach>", self.__ev_element_detached, lambda event, object_id : True)
            element._parent = self
        for element in [e for e in self.__elements if e not in my_list]:
            element.remove_event("<Detach>", self.__ev_element_detached, lambda event, object_id : True)
            element._parent = None
            element.pos = vector2d(0, 0)
            element.visible = False
        self.__elements = my_list
        self.__place_elements()
    
    def __ev_element_detached(self, params):
        my_object = params.get("object_id")
        if type(my_object) not in [ETKListingContainer, ETKContainer]:
            for element in self.__elements:
                if element.object_id == my_object:
                    my_object = element
                    break
        self.__elements.remove(my_object)
        my_object.anchor = vector2d()
        my_object.pos = vector2d()
        my_object.visible = False
    
    def detach(self):
        self._eventhandler("<Detach>")
    ######
    ######
    ######


    ######
    ###methods as parent###
    ######

    def _get_pos_in_parent(self, child)->vector2d:    
        return child.abs_pos - self.pos
    
    def _validate(self, action:str, child)->bool:
        if action == "move":
            if self.__mov_flag:
                self.__mov_flag = False
                return True
            return False
        
        if action == "visible":
            return self.visible
        
        return True
    
    def _element_changed(self, child):
        self.__place_elements()
    ######
    ######
    ######