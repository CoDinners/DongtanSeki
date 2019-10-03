from pygame import draw
from pygame.surface import Surface

from src.Constants import FONT_PATH, BLUE_COLOR
from src.Font import Font
from src.Positioning import center
from src.manager.MouseManager import MouseManager
from src.root_object.RootObject import RootObject
from src.root_object.Text import Text


class ButtonRect(RootObject):
    def __init__(self, x, y, width, height, normal_color, pressd_color, text, mouse_manager: MouseManager):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.normal_color = normal_color
        self.pressed_color = pressd_color
        self.text = text
        self.mouse_manager: MouseManager = mouse_manager

        font = Font(FONT_PATH, 96, BLUE_COLOR)

        self.text_object = Text(0, 0, self.text, font)
        self.text_object.x = center(self.width, self.text_object.surface.get_width()) + self.x
        self.text_object.y = center(self.height, self.text_object.surface.get_height()) + self.y

        self.pressed = False
        self.previous_pressed = False
        self.start_pressed = False

    def tick(self):
        self.previous_pressed = self.pressed

        self.pressed = (self.mouse_manager.left and
                        self.x <= self.mouse_manager.x <= self.x + self.width and
                        self.y <= self.mouse_manager.y <= self.y + self.height)

        self.start_pressed = not self.previous_pressed and self.pressed

    def render(self, surface: Surface):
        draw.rect(surface, self.pressed_color if self.pressed else self.normal_color,
                  ((self.x, self.y), (self.width, self.height)))
        self.text_object.render(surface)
