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
        if self.parent != None:
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
        vec_mask, dynamic_dim = self.__get_mask_vec_and_dynamic_dim()

        my_dim = self.__dimensions

        self.__dimensions = vector2d(dynamic_dim.x if self.__dimensions.x == -1 else self.__dimensions.x,
                                     dynamic_dim.y if self.__dimensions.y == -1 else self.__dimensions.y)

        if (dynamic_dim * vec_mask.switch(False)).lenght > (self.__dimensions * vec_mask.switch(False)).lenght:
            return #raise Error
        
        if self.__listing_type in [ListingTypes.BOTTOM_TO_TOP, ListingTypes.RIGHT_TO_LEFT]:
            self.__elements.reverse()
        index = 0
        visible_elements = []
        for element in self.__elements:
            if not element.visible:
                continue
            visible_elements.append(element)
            new_pos = self.__calc_child_pos(index, dynamic_dim * vec_mask, vec_mask, visible_elements)
            if new_pos == None:
                break
            element.pos = new_pos
            index += 1
        if self.__listing_type in [ListingTypes.BOTTOM_TO_TOP, ListingTypes.RIGHT_TO_LEFT]:
            self.__elements.reverse()
        
        self.__dimensions = my_dim

    def __calc_child_pos(self, index:int, dynamic_dim:vector2d, vec_mask:vector2d, element_list:list)->vector2d:
        my_element = element_list[-1]
        #calculate the vector that defines the box,
        #that the unary component of the child forms with the lenght of all the listed childs in the other axi
        bounding_box_dim = dynamic_dim * vec_mask + vector2d(my_element.width,my_element.height) * vec_mask.switch(False)
        #adds the widths and heigts of other elemts, to get the offset from the top left if 
        listed_offset_by_index = self.__vector_sum([vector2d(event.width, event.height) for event in element_list[:-1]])
        #apply the offset between the widgets
        listed_offset_by_index += vector2d(1,1).normalize() * index * self.__offset * 2
        #catch if element would be outside the container
        if (self.__vector_sum([vector2d(event.width, event.height) for event in element_list]) * vec_mask).lenght + index * self.__offset > (self.__dimensions * vec_mask).lenght:
            print(f"Warning, too many elements, were inputted in container, skipping all elemnts after element{index}")
            return None
        #calculate the vector that is dependent on the listing type of the Container
        case_sensitive_vec = -1 * bounding_box_dim * self.__alignment_type + listed_offset_by_index * (vec_mask * 2)
        #calculate the final position of the element
        return self.__my_pos + (self.__dimensions * self.__alignment_type + case_sensitive_vec) / 2
    
    def __get_mask_vec_and_dynamic_dim(self):
        if self.__listing_type in [ListingTypes.TOP_TO_BOTTOM, ListingTypes.BOTTOM_TO_TOP]:
            dim_max = max([event.width for event in self.__elements])
            vec_mask = vector2d(0, 1)
        if self.__listing_type in [ListingTypes.LEFT_TO_RIGHT, ListingTypes.RIGHT_TO_LEFT]:
            dim_max = max([event.height for event in self.__elements])
            vec_mask = vector2d(1, 0)
        dim_vec_sum = self.__vector_sum([vector2d(e.width, e.height) for e in self.__elements if e.visible])
        dim_sum = (dim_vec_sum * vec_mask).lenght + self.__offset * (len(self.__elements) - 1)

        dynamic_dim = vector2d(dim_sum if vec_mask.x else dim_max,
                               dim_sum if vec_mask.y else dim_max)
        
        return vec_mask, dynamic_dim
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