from pygame.surface import Surface

from src.Display import Display


class State:
    background_color = (0, 0, 0)

    def tick(self):
        pass

    def render(self, surface: Surface):
        pass

    def resize(self, display: Display):
        pass
