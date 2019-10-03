from pickle import dump, load

from pygame.surface import Surface

from src.Constants import IVORY_COLOR, RED_COLOR, BLUE_COLOR, FONT_PATH, BLACK_COLOR
from src.Display import Display
from src.Font import Font
from src.manager.MouseManager import MouseManager
from src.root_object.ClickArea import ClickArea
from src.root_object.ClickReverseSquare import ClickReverseSquare
from src.root_object.ObjectMover import ObjectMover
from src.root_object.Rectangle import Rectangle
from src.root_object.Text import Text
from src.root_object.Transition import Transition
from src.state.State import State


class Collocate(State):
    background_color = IVORY_COLOR

    SEATS = './res/seats.pickle'

    def __init__(self, display: Display, mouse_manager: MouseManager, state_manager):
        self.state_manager = state_manager

        self.square_size = (display.height - 300) * 6 / 41
        self.square_gap = self.square_size / 6

        self.squares = []

        data = load(open(Collocate.SEATS, 'rb'))
        for y in range(6):
            self.squares.append([])
            for x in range(10):
                self.squares[y].append(
                    ClickReverseSquare(
                        150 + x * (self.square_size + self.square_gap), 150 + y * (self.square_size + self.square_gap),
                        self.square_size, RED_COLOR, BLUE_COLOR, mouse_manager, data[y][x]))
        del data

        self.upper_rect = Rectangle(150, 84, (self.square_size + self.square_gap) * 9 + self.square_size, 42, BLUE_COLOR, display)
        self.lower_rect = Rectangle(150, display.height - 128,
                                    (self.square_size + self.square_gap) * 9 + self.square_size, 42, RED_COLOR, display)

        button_font = Font(FONT_PATH, 96, BLACK_COLOR)
        self.ok_button = Text(0, 0, '완료', button_font)
        self.ok_button.x = display.width - 150 - self.ok_button.surface.get_width()
        self.ok_button.y = display.height / 2 - self.square_size - self.square_gap - self.ok_button.font.size
        self.ok_button_clickarea = ClickArea(
            mouse_manager, self.ok_button.surface.get_width(), self.ok_button.surface.get_height(),
            sticker=self.ok_button
        )

        self.cancel_button = Text(0, 0, '취소', button_font)
        self.cancel_button.x = display.width - 150 - self.cancel_button.surface.get_width()
        self.cancel_button.y = display.height / 2 + self.square_size + self.square_gap
        self.cancel_button_clickarea = ClickArea(
            mouse_manager, self.cancel_button.surface.get_width(), self.cancel_button.surface.get_height(),
            sticker=self.cancel_button
        )
        self.button_transition = Transition(BLUE_COLOR, display, after=self._button_transition_after)

        self.barrier_rect = Rectangle(
            -(150 + (self.square_size + self.square_gap) * 10), 0, 150 + (self.square_size + self.square_gap) * 10, display.height, Collocate.background_color, display)

        self.object_movers = [
            ObjectMover(self.ok_button, initial_offset_x=(150 + self.ok_button.surface.get_width()) * 2),
            ObjectMover(self.cancel_button, initial_offset_x=(150 + self.cancel_button.surface.get_width()) * 2),
            ObjectMover(self.barrier_rect, initial_offset_x=(150 + (self.square_size + self.square_gap) * 10))
        ]

    def tick(self):
        for object_mover in self.object_movers:
            object_mover.tick()

        for y in range(6):
            for x in range(10):
                self.squares[y][x].tick()

        self.ok_button_clickarea.tick()
        self.cancel_button_clickarea.tick()

        if self.cancel_button_clickarea.clicked:
            self.button_transition.start()
        elif self.ok_button_clickarea.clicked:
            data = []
            for y in range(len(self.squares)):
                data.append([])
                for x in range(len(self.squares[y])):
                    data[y].append(self.squares[y][x].state)
            dump(data, open(Collocate.SEATS, 'wb'))
            self.button_transition.start()

        self.button_transition.tick()

    def _button_transition_after(self):
        self.state_manager.set_state('lobby')

    def render(self, surface: Surface):
        for y in range(6):
            for x in range(10):
                self.squares[y][x].render(surface)

        self.barrier_rect.render(surface)

        self.upper_rect.render(surface)
        self.lower_rect.render(surface)

        self.ok_button.render(surface)
        self.cancel_button.render(surface)

        self.button_transition.render(surface)
