from pygame import display, image
from pygame.time import Clock


class Display:
    def __init__(self, width: int, height: int, title: str, fps: float, icon_path: str):
        self.width: int = width
        self.height: int = height
        self.title: str = title
        self.fps: float = fps
        self.icon_path: str = icon_path

        display.set_caption(self.title)
        display.set_icon(image.load(icon_path))

        self.window = display.set_mode((self.width, self.height))

        self.clock = Clock()
