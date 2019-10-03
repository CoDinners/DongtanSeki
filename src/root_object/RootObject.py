from pygame.surface import Surface

from src.Display import Display


class RootObject:
    def tick(self):
        pass

    def render(self, surface: Surface):
        pass

    def resize(self, display: Display):
        pass
