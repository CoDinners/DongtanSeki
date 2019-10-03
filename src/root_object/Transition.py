from time import time

from pygame import gfxdraw
from pygame.surface import Surface

from src.Display import Display
from src.root_object.RootObject import RootObject


def get_progress_by_timing(x: float) -> float:
    return -(x - 1) ** 4 + 1


class Transition(RootObject):
    def __init__(self, color: tuple, display: Display, duration: float = 1.0, after=None):
        self.color = color
        self.display = display
        self.duration = duration
        self.after = after

        self.start_time = 0

        self.started = False
        self.end = False

        self.rhombus = 0
        self.rhombus_max = (min(display.width, display.height) + max(display.width, display.height)) / 2

    def start(self):
        self.start_time = time()
        self.started = True

    def tick(self):
        if self.started:
            now = time()

            delta_time = now - self.start_time

            if delta_time >= self.duration:
                self.end = True
                if self.after is not None:
                    self.after()

            if not self.end:
                progress = get_progress_by_timing(delta_time / self.duration)
                self.rhombus = self.rhombus_max * progress

    def render(self, surface: Surface):
        gfxdraw.filled_polygon(surface, (
            (self.display.width / 2, self.display.height / 2 - self.rhombus),
            (self.display.width / 2 + self.rhombus, self.display.height / 2),
            (self.display.width / 2, self.display.height / 2 + self.rhombus),
            (self.display.width / 2 - self.rhombus, self.display.height / 2)
        ), self.color)
