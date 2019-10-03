from pygame import draw
from pygame.surface import Surface

from src.Constants import FONT_PATH, BLUE_COLOR
from src.Font import Font
from src.Positioning import center
from src.root_object.RootObject import RootObject
from src.root_object.Text import Text


class TextIndexSelector(RootObject):
    def __init__(self, x, y, width, height, normal_color, selector_color, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.normal_color = normal_color
        self.selected_color = selector_color
        self.text = text

        self.selected = False
        self.text_object = None
        self.refresh_text()

    def set_text(self, text):
        self.text = str(int(text))
        self.refresh_text()

    def refresh_text(self):
        self.text_object = Text(0, 0, self.text, Font(FONT_PATH, 96, BLUE_COLOR))
        self.text_object.x = center(self.width, self.text_object.surface.get_width()) + self.x
        self.text_object.y = center(self.height, self.text_object.surface.get_height()) + self.y

    def render(self, surface: Surface):
        draw.rect(surface, self.selected_color if self.selected else self.normal_color, ((self.x, self.y), (self.width, self.height)))

        self.text_object.render(surface)
