from math import hypot
from pickle import load
from random import choice

from pygame.surface import Surface

from src.Constants import RED_COLOR, FONT_PATH, IVORY_COLOR, BLUE_COLOR
from src.Display import Display
from src.Font import Font
from src.Positioning import center
from src.manager.MouseManager import MouseManager
from src.root_object.ClickArea import ClickArea
from src.root_object.ObjectMover import ObjectMover
from src.root_object.PushOpenRectangle import PushOpenRectangle
from src.root_object.Text import Text
from src.root_object.Transition import Transition
from src.state.Collocate import Collocate
from src.state.Secret import Secret
from src.state.State import State


def generate_seat_arrangement(available: list) -> tuple:
    result = []

    count = 0

    for y in range(len(available)):
        for x in range(len(available[y])):
            if available[y][x]:
                count += 1

    numbers = list(range(1, count + 1))

    for y in range(len(available)):
        result.append([])
        for x in range(len(available[y])):
            if available[y][x]:
                number = choice(numbers)
                result[y].append(number)
                numbers.remove(number)
            else:
                result[y].append(0)

    def find(value, _list):
        for _y in range(len(_list)):
            for _x in range(len(_list[_y])):
                if _list[_y][_x] == value:
                    return _x, _y

    secret = load(open(Secret.SAVE_PATH, 'rb'))

    friend_bound = 1.5
    ban_bound = 2.1

    if secret[0][0]:
        center = find(secret[0][0], result)
        for friend in secret[0][1]:
            if not friend: continue
            friend_position = find(friend, result)
            if hypot(friend_position[0] - center[0], friend_position[1] - center[1]) > friend_bound:
                return generate_seat_arrangement(available)
        for ban in secret[0][2]:
            if not ban: continue
            ban_position = find(ban, result)
            if hypot(ban_position[0] - center[0], ban_position[1] - center[1]) <= ban_bound:
                return generate_seat_arrangement(available)
    if secret[1][0]:
        center = find(secret[1][0], result)
        for friend in secret[1][1]:
            if not friend: continue
            friend_position = find(friend, result)
            if hypot(friend_position[0] - center[0], friend_position[1] - center[1]) > friend_bound:
                return generate_seat_arrangement(available)
        for ban in secret[1][2]:
            if not ban: continue
            ban_position = find(ban, result)
            if hypot(ban_position[0] - center[0], ban_position[1] - center[1]) <= ban_bound:
                return generate_seat_arrangement(available)

    return result


class Place(State):
    background_color = RED_COLOR

    def __init__(self, display: Display, mouse_manager: MouseManager, state_manager):
        self.display = display
        self.mouse_manager = mouse_manager
        self.state_manager = state_manager

        self.leave_button = Text(50, display.height - 122, '나가기', Font(FONT_PATH, 72, IVORY_COLOR))
        self.leave_button_clickarea = ClickArea(
            self.mouse_manager, self.leave_button.surface.get_width(), self.leave_button.surface.get_height(),
            sticker=self.leave_button
        )
        self.leave_button_transition = Transition(BLUE_COLOR, self.display, after=self._leave_button_transition)

        self.object_movers = (
            ObjectMover(self.leave_button,
                        initial_offset_x=-(self.leave_button.x + self.leave_button.surface.get_width()) * 2),)

        data = load(open(Collocate.SEATS, 'rb'))
        while True not in data[-1]:
            del data[-1]

        while True:
            delete = True
            for i in range(len(data)):
                if data[i][-1]:
                    delete = False
            if delete:
                for i in range(len(data)):
                    data[i] = data[i][:-1]
            else:
                break

        height, width = len(data), len(data[0])

        place = generate_seat_arrangement(data)

        size = (display.height - 300) * height / (height * height + height - 1)
        gap = size / height

        # self.a = PushOpenRectangle(100, 100, size, size, IVORY_COLOR, BLUE_COLOR, '29', self.mouse_manager)
        pixel_width = width * (size + gap) - gap
        pixel_height = height * (size + gap) - gap

        x, y = center(self.display.width, pixel_width), center(self.display.height, pixel_height)

        self.push_open_rectangles = []
        for yi in range(len(place)):
            for xi in range(len(place[yi])):
                if place[yi][xi]:
                    self.push_open_rectangles.append(
                        PushOpenRectangle(x + xi * (size + gap), y + yi * (size + gap), size, size,
                                          IVORY_COLOR, IVORY_COLOR, str(place[yi][xi]), self.mouse_manager))

    def tick(self):
        for object_mover in self.object_movers:
            object_mover.tick()

        self.leave_button_clickarea.tick()

        if self.leave_button_clickarea.clicked:
            self.leave_button_transition.start()

        self.leave_button_transition.tick()

        for push_open_rectangle in self.push_open_rectangles:
            push_open_rectangle.tick()

    def _leave_button_transition(self):
        self.state_manager.set_state('lobby')

    def render(self, surface: Surface):
        self.leave_button.render(surface)

        for push_open_rectangle in self.push_open_rectangles:
            push_open_rectangle.render(surface)

        self.leave_button_transition.render(surface)
