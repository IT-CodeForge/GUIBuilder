from generator.TGW_generator import*
if __name__ == "__main__":
    #code which tests evry functionality
    myGenerator = TGW_Generator()
    objects = [{"type": "window", "position": [10,10], "size": [1024,512], "text": "Hallo", "backgroundColor": [12,23,34], "eventMouseMove": True},
               {"type": "button", "name": "einKnopf", "position": [10,10], "size": [128, 32], "text": "Knopf", "eventPressed": True},
               {"type": "checkbox", "name": "meineCheckbox", "position": [10,52], "size": [128,32], "text": "ich bin eine Checkbox", "eventChanged": True, "checked": False},
               {"id": 0, "type": "timer", "name": "einTimer", "interval": 1000, "enabled": True},
               {"type": "canvas", "name": "einCanvas", "position": [148,10], "size": [138,138], "backgroundColor": [255,0,0]},
               {"type": "label", "name": "einLabel", "position": [10, 94], "size": [12, 128], "text": "Ich bin ein label"},
               {"type": "edit", "name": "Edit2", "position": [148, 94], "size": [12, 128], "text": "Ich bin ein edit", "multipleLines": True, "eventChanged": True}]
    myGenerator.write_files("", objects)