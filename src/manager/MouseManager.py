from pygame import mouse


class MouseManager:
    def __init__(self):
        self.x = 0
        self.y = 0

        self.left = False
        self.previous_left = False
        self.start_left = False
        self.end_left = False

        self.wheel = False
        self.previous_wheel = False
        self.start_wheel = False
        self.end_wheel = False

        self.right = False
        self.previous_right = False
        self.start_right = False
        self.end_right = False

    def handle(self):
        self.left, self.wheel, self.right = mouse.get_pressed()
        self.x, self.y = mouse.get_pos()

    def tick(self):
        self.start_left = not self.previous_left and self.left
        self.end_left = self.previous_left and not self.left
        
        self.start_wheel = not self.previous_wheel and self.wheel
        self.end_wheel = self.previous_wheel and not self.wheel
        
        self.start_right = not self.previous_right and self.right
        self.end_right = self.previous_right and not self.right
        
        self.previous_left = self.left
        self.previous_wheel = self.wheel
        self.previous_wheel = self.right
