from pygame import draw
from pygame.surface import Surface

from src.Constants import FONT_PATH, RED_COLOR
from src.Font import Font
from src.Positioning import center
from src.manager.MouseManager import MouseManager
from src.root_object.RootObject import RootObject
from src.root_object.Text import Text


class PushOpenRectangle(RootObject):
    def __init__(self, x, y, width, height, opened_background, closed_color, text, mouse_manager: MouseManager):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.opened_background = opened_background
        self.closed_color = closed_color
        self.text = text
        self.mouse_manager = mouse_manager

        font = Font(FONT_PATH, 96, RED_COLOR)

        self.text_object = Text(0, 0, self.text, font)
        self.text_object.x = center(self.width, self.text_object.surface.get_width()) + self.x
        self.text_object.y = center(self.height, self.text_object.surface.get_height()) + self.y

        self.opened = False

    def tick(self):
        if self.mouse_manager.end_left and \
                self.x <= self.mouse_manager.x <= self.x + self.width and \
                self.y <= self.mouse_manager.y <= self.y + self.height:
            self.opened = not self.opened

    def render(self, surface: Surface):
        if self.opened:
            draw.rect(surface, self.opened_background, ((self.x, self.y), (self.width, self.height)))
            self.text_object.render(surface)
        else:
            draw.rect(surface, self.closed_color, ((self.x, self.y), (self.width, self.height)))
