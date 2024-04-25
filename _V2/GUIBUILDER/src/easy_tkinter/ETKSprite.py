from .ETKCanvas        import ETKCanvas
from .ETKCanvasItem    import ETKCanvasItem
from .vector2d        import vector2d
import math
import json

class ETKSprite:
    def __init__(self) -> None:
        self.sprite_list = []
        self.anchor = vector2d()
    
    def move(self, mov_vec:vector2d):
        for canvas_item in self.sprite_list:
            canvas_item.move(mov_vec)

    def move_to(self, pos:vector2d):
        self.move(pos - self.anchor)

    def rotate_with_radians(self, radians:float):
        for canvas_item in self.sprite_list:
            canvas_item.anchor = (canvas_item.anchor - self.anchor).rotate(radians) + self.anchor
            canvas_item.rotate_with_radians(radians)
    
    def rotate_with_degrees(self, degrees:float):
        self.rotate_with_radians(degrees * math.pi / 180)

    def group_as_sprite(self, canvas_item_list:list[ETKCanvasItem], sprite_anchor:vector2d=vector2d(0,0)):
        self.sprite_list = canvas_item_list

    def load_sprite(self, file_path_with_file_name:str, canvas:ETKCanvas):
        self.delete_sprite_data()
        with open(file_path_with_file_name, "r") as openfile:
            json_object = json.load(openfile)
            for canvas_item_data in json_object:
                canvas_item = ETKCanvasItem(canvas, "json" + canvas_item_data.get("item_type"), canvas_item_data)
                self.sprite_list.append(canvas_item)

    def save_as(self, file_path_with_file_name:str):
        json_list = []
        for canvas_item in self.sprite_list:
            canvas_item_dict = {
                "item_type":canvas_item.get_item_type(),
                "col":canvas_item.fill,
                "line_col":canvas_item.line_col,
                "thickness":canvas_item.thickness,
                "pointlist":canvas_item.pointlist}
            json_list.append(canvas_item_dict)
        json_str = json.dumps([{"item_type"}])
        with open(file_path_with_file_name, "w") as openfile:
            openfile.write(json_list)

    def delete_sprite_data(self):
        for canvas_item in self.sprite_list:
            canvas_item = self.sprite_list.pop()
            del canvas_item
    
    def __del__(self):
        self.delete_sprite()