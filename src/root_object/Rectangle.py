from pygame import draw
from pygame.surface import Surface

from src.Display import Display
from src.root_object.RootObject import RootObject


class Rectangle(RootObject):
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple, display: Display):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.display = display

        self.optimized_state = True
        self.optimized_x = x
        self.optimized_y = y
        self.optimized_width = width
        self.optimized_height = height

    def tick(self):
        self.optimized_state = (self.x > self.display.width or self.y > self.display.height or
                                self.x + self.width < 0 or self.y + self.height < 0)
        if self.optimized_state:
            self.optimized_x = max(self.x, 0)
            self.optimized_y = max(self.y, 0)
            if self.x < 0:
                self.optimized_width = self.width - abs(self.x)
            if self.y < 0:
                self.optimized_height = self.height - abs(self.y)
            if self.x + self.width > self.display.width:
                self.width = self.display.width - self.x
            if self.y + self.height > self.display.height:
                self.height = self.display.height - self.y

    def render(self, surface: Surface):
        if self.optimized_state:
            draw.rect(surface, self.color, ((self.x, self.y), (self.width, self.height)))
