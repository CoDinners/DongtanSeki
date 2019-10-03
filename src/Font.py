from pygame.font import Font as _Font
from pygame.surface import Surface


class Font:
    def __init__(self, path: str, size: int, color: tuple):
        self.path = path
        self.size = size
        self.color = color

        self.font: _Font = None
        self.refresh_font()

    def render(self, text: str) -> Surface:
        return self.font.render(text, True, self.color)

    def refresh_font(self):
        self.font = _Font(self.path, self.size)

    def set_size(self, size: int):
        self.size = size
        self.refresh_font()

    def set_color(self, color: tuple):
        self.color = color
        self.refresh_font()
