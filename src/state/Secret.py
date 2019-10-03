from pickle import load, dump

from pygame.surface import Surface

from src import Display
from src.Constants import BLACK_COLOR, IVORY_COLOR, RED_COLOR
from src.manager.MouseManager import MouseManager
from src.root_object.ButtonRect import ButtonRect
from src.root_object.TextIndexSelector import TextIndexSelector
from src.state.State import State


class Secret(State):
    background_color = BLACK_COLOR

    SAVE_PATH = './res/secret.pickle'

    def __init__(self, display: Display, mouse_manager: MouseManager, state_manager):
        self.mouse_manager = mouse_manager
        self.state_manager = state_manager

        self.keypads = (
            ButtonRect(display.width - 699, display.height / 2 + 218, 348, 150,
                       IVORY_COLOR, RED_COLOR, '0', mouse_manager),
            ButtonRect(display.width - 699, display.height / 2 + 20, 150, 150,
                       IVORY_COLOR, RED_COLOR, '1', mouse_manager),
            ButtonRect(display.width - 501, display.height / 2 + 20, 150, 150,
                       IVORY_COLOR, RED_COLOR, '2', mouse_manager),
            ButtonRect(display.width - 303, display.height / 2 + 20, 150, 150,
                       IVORY_COLOR, RED_COLOR, '3', mouse_manager),
            ButtonRect(display.width - 699, display.height / 2 - 178, 150, 150,
                       IVORY_COLOR, RED_COLOR, '4', mouse_manager),
            ButtonRect(display.width - 501, display.height / 2 - 178, 150, 150,
                       IVORY_COLOR, RED_COLOR, '5', mouse_manager),
            ButtonRect(display.width - 303, display.height / 2 - 178, 150, 150,
                       IVORY_COLOR, RED_COLOR, '6', mouse_manager),
            ButtonRect(display.width - 699, display.height / 2 - 376, 150, 150,
                       IVORY_COLOR, RED_COLOR, '7', mouse_manager),
            ButtonRect(display.width - 501, display.height / 2 - 376, 150, 150,
                       IVORY_COLOR, RED_COLOR, '8', mouse_manager),
            ButtonRect(display.width - 303, display.height / 2 - 376, 150, 150,
                       IVORY_COLOR, RED_COLOR, '9', mouse_manager),
            ButtonRect(display.width - 303, display.height / 2 + 218, 150, 150,
                       IVORY_COLOR, RED_COLOR, 'X', mouse_manager)
        )

        data = load(open(Secret.SAVE_PATH, 'rb'))

        self.point1 = TextIndexSelector(150, 150, 150, 150, IVORY_COLOR, RED_COLOR, str(data[0][0]))
        self.friendlies1 = [
            TextIndexSelector(388, 150, 150, 150, IVORY_COLOR, RED_COLOR, str(data[0][1][0])),
            TextIndexSelector(567, 150, 150, 150, IVORY_COLOR, RED_COLOR, str(data[0][1][1])),
            TextIndexSelector(746, 150, 150, 150, IVORY_COLOR, RED_COLOR, str(data[0][1][2])),
            TextIndexSelector(925, 150, 150, 150, IVORY_COLOR, RED_COLOR, str(data[0][1][3]))
        ]
        self.bans1 = [
            TextIndexSelector(388, 327, 150, 150, IVORY_COLOR, RED_COLOR, str(data[0][2][0])),
            TextIndexSelector(567, 327, 150, 150, IVORY_COLOR, RED_COLOR, str(data[0][2][1])),
            TextIndexSelector(746, 327, 150, 150, IVORY_COLOR, RED_COLOR, str(data[0][2][2])),
            TextIndexSelector(925, 327, 150, 150, IVORY_COLOR, RED_COLOR, str(data[0][2][3]))
        ]
        self.point2 = TextIndexSelector(150, 603, 150, 150, IVORY_COLOR, RED_COLOR, str(data[1][0]))
        self.friendlies2 = [
            TextIndexSelector(388, 603, 150, 150, IVORY_COLOR, RED_COLOR, str(data[1][1][0])),
            TextIndexSelector(567, 603, 150, 150, IVORY_COLOR, RED_COLOR, str(data[1][1][1])),
            TextIndexSelector(746, 603, 150, 150, IVORY_COLOR, RED_COLOR, str(data[1][1][2])),
            TextIndexSelector(925, 603, 150, 150, IVORY_COLOR, RED_COLOR, str(data[1][1][3]))
        ]
        self.bans2 = [
            TextIndexSelector(388, 780, 150, 150, IVORY_COLOR, RED_COLOR, str(data[1][2][0])),
            TextIndexSelector(567, 780, 150, 150, IVORY_COLOR, RED_COLOR, str(data[1][2][1])),
            TextIndexSelector(746, 780, 150, 150, IVORY_COLOR, RED_COLOR, str(data[1][2][2])),
            TextIndexSelector(925, 780, 150, 150, IVORY_COLOR, RED_COLOR, str(data[1][2][3]))
        ]

        self.selected = None

    def tick(self):
        if self.mouse_manager.end_left and self.mouse_manager.x < 150:
            dump([
                [
                    int(self.point1.text),
                    [int(self.friendlies1[i].text) for i in range(len(self.friendlies1))],
                    [int(self.bans1[i].text) for i in range(len(self.bans1))]
                ], [
                    int(self.point2.text),
                    [int(self.friendlies2[i].text) for i in range(len(self.friendlies2))],
                    [int(self.bans2[i].text) for i in range(len(self.bans2))]
                ]], open(Secret.SAVE_PATH, 'wb'))
            self.state_manager.set_state('lobby')

        if self.mouse_manager.left and self.mouse_manager.x < self.bans2[-1].x + self.bans2[-1].width:
            self.selected = None
            selectors = [self.point1] + self.friendlies1 + self.bans1 + [self.point2] + self.friendlies2 + self.bans2
            for selector in selectors:
                selector.selected = False
                if selector.x <= self.mouse_manager.x <= selector.x + selector.width and \
                        selector.y <= self.mouse_manager.y <= selector.y + selector.height:
                    self.selected = selector
                    selector.selected = True

        for keypad in self.keypads:
            keypad.tick()
            if keypad.start_pressed:
                if self.selected is not None:
                    if keypad.text != 'X':
                        self.selected.set_text(self.selected.text + keypad.text)
                    else:
                        self.selected.set_text('0')

    def render(self, surface: Surface):
        for keypad in self.keypads:
            keypad.render(surface)

        self.point1.render(surface)
        for friendly in self.friendlies1:
            friendly.render(surface)
        for ban in self.bans1:
            ban.render(surface)
        self.point2.render(surface)
        for friendly in self.friendlies2:
            friendly.render(surface)
        for ban in self.bans2:
            ban.render(surface)
