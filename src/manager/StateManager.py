from pygame.surface import Surface

from src.state.Collocate import Collocate
from src.state.Lobby import Lobby
from src.state.Place import Place
from src.state.State import State


class StateManager:
    def __init__(self, shutdown, display, mouse_manager, initial_state: State = None):
        self.shutdown = shutdown
        self.display = display
        self.mouse_manager = mouse_manager
        self.state: State = initial_state

    def set_state(self, state_name: str):
        if state_name == 'lobby':
            self.state = Lobby(self.shutdown, self.display, self.mouse_manager, self)
        elif state_name == 'collocate':
            self.state = Collocate(self.display, self.mouse_manager, self)
        elif state_name == 'place':
            self.state = Place()

    def tick(self):
        self.state.tick()

    def render(self, surface: Surface):
        self.state.render(surface)
