from pygame.surface import Surface

from src.Font import Font
from src.root_object.RootObject import RootObject


class Text(RootObject):
    def __init__(self, x: int, y: int, text: str, font: Font):
        self.x = x
        self.y = y
        self.text = text
        self.font = font

        self.surface = self.font.render(self.text)

    def render(self, surface: Surface):
        surface.blit(self.surface, (self.x, self.y))
