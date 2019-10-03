from src.root_object.RootObject import RootObject


class ObjectMover(RootObject):
    def __init__(self, _object, *, initial_offset_x=0, initial_offset_y=0, friction: float = 6.0):
        self.object = _object
        self.target_x = self.object.x
        self.target_y = self.object.y
        self.friction = friction

        self.object.x += initial_offset_x
        self.object.y += initial_offset_y

    def tick(self):
        self.object.x += (self.target_x - self.object.x) / self.friction
        self.object.y += (self.target_y - self.object.y) / self.friction
