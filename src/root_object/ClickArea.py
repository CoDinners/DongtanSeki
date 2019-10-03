from src.manager.MouseManager import MouseManager
from src.root_object.RootObject import RootObject


class ClickArea(RootObject):
    def __init__(self, mouse_manager: MouseManager, width=0, height=0, x=0, y=0, sticker=None):
        self.mouse_manager = mouse_manager
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sticker = sticker

        self.clicked = False

    def tick(self):
        if self.sticker:
            self.x = self.sticker.x
            self.y = self.sticker.y

        self.clicked = (self.mouse_manager.end_left and
                        self.x <= self.mouse_manager.x <= self.x + self.width and
                        self.y <= self.mouse_manager.y <= self.y + self.height)
