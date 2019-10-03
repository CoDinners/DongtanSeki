from pygame import display
from pygame.time import Clock


class Display:
    def __init__(self, width: int, height: int, title: str, fps: float):
        self.width: int = width
        self.height: int = height
        self.title: str = title
        self.fps: float = fps

        self.window = display.set_mode((self.width, self.height))

        self.clock = Clock()
