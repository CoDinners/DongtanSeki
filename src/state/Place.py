from src.Constants import RED_COLOR
from src.manager.MouseManager import MouseManager
from src.state.State import State


class Place(State):
    background_color = RED_COLOR

    def __init__(self, mouse_manager: MouseManager, state_manager):
        self.mouse_manager = mouse_manager
        self.state_manager = state_manager

    def tick(self):
        if self.mouse_manager.left and self.mouse_manager.right:
            self.state_manager.set_state('secret')
