from pygame import draw
from pygame.surface import Surface

from src.manager.MouseManager import MouseManager
from src.root_object.RootObject import RootObject


class ClickReverseSquare(RootObject):
    def __init__(self, x: int, y: int, size: int, color_false: bool, color_true: bool, mouse_manager: MouseManager,
                 initial_state: bool = False):
        self.x = x
        self.y = y
        self.size = size
        self.color_false = color_false
        self.color_true = color_true
        self.mouse_manager = mouse_manager

        self.state = initial_state

    def tick(self):
        if self.mouse_manager.start_left and \
                self.x <= self.mouse_manager.x <= self.x + self.size and \
                self.y <= self.mouse_manager.y <= self.y + self.size:
            self.state = not self.state

    def render(self, surface: Surface):
        draw.rect(surface, self.color_true if self.state else self.color_false, ((self.x, self.y), (self.size,) * 2))
