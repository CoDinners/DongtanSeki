import pygame

from src.Constants import PROJECT_NAME
from src.Display import Display
from src.manager.MouseManager import MouseManager
from src.manager.RootObjectManager import RootObjectManager
from src.manager.StateManager import StateManager

running = False
display: Display = None

mouse_manager: MouseManager = None
object_manager: RootObjectManager = None
state_manager: StateManager = None

def shutdown():
    global running

    running = False

def init():
    global display, running, mouse_manager, object_manager, state_manager

    pygame.init()

    running = True
    display = Display(1920, 1080, PROJECT_NAME, 60, './res/icon.png')

    mouse_manager = MouseManager()
    object_manager = RootObjectManager()
    state_manager = StateManager(shutdown, display, mouse_manager)

    state_manager.set_state('lobby')

def handle():
    mouse_manager.handle()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            shutdown()

def tick():
    mouse_manager.tick()

    state_manager.tick()

def render(surface: pygame.Surface):
    surface.fill(state_manager.state.background_color)
    state_manager.render(surface)

    pygame.display.flip()

def main():
    init()
    while running:
        handle()
        tick()
        render(display.window)

        display.clock.tick(display.fps)
    pygame.quit()
