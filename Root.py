import pygame

from Display import Display

running = False
display = None

def init():
    global display, running

    running = True
    display = Display(1280, 720, 'DongtanSeat', 60)

def handle():
    pass

def tick():
    pass

def render(surface: pygame.Surface):
    pass

def main():
    init()
    while running:
        handle()
        tick()
        render(display.window)
    pygame.quit()
