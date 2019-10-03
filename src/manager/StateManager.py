from pygame.surface import Surface

from src.state.State import State


class StateManager:
    def __init__(self, initial_state: State = None):
        self.state: State = initial_state

    def set_state(self, state: State):
        self.state = state

    def tick(self):
        self.state.tick()

    def render(self, surface: Surface):
        self.state.render(surface)
