from pygame.surface import Surface

from src.root_object.RootObject import RootObject


class RootObjectManager:
    def __init__(self):
        self.objects = []

    def add(self, _object: RootObject):
        self.objects.append(_object)

    def tick(self):
        for _object in self.objects:
            _object.tick()

    def render(self, surface: Surface):
        for _object in self.objects:
            _object.render(surface)
