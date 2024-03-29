from pygame.surface import Surface

from src.Constants import BLUE_COLOR, IVORY_COLOR, FONT_PATH, RED_COLOR, PROJECT_NAME
from src.Display import Display
from src.Font import Font
from src.manager.MouseManager import MouseManager
from src.root_object.ClickArea import ClickArea
from src.root_object.ObjectMover import ObjectMover
from src.root_object.Text import Text
from src.root_object.Transition import Transition
from src.state.State import State


class Lobby(State):
    background_color = BLUE_COLOR

    def __init__(self, shutdown, display: Display, mouse_manager: MouseManager, state_manager):
        self.shutdown = shutdown
        self.display = display
        self.mouse_manager = mouse_manager
        self.state_manager = state_manager

        self.text_color = IVORY_COLOR

        copyright_font = Font(FONT_PATH, 24, self.text_color)
        self.copyright1 = Text(150, self.display.height - 150 - copyright_font.size * 2 - 6,
                               'Copyright (c) 2014-2019 David "Sch" Jeon.', copyright_font)
        self.copyright2 = Text(150, self.display.height - 150 - copyright_font.size,
                               'All rights belong to its respective owners.', copyright_font)

        title_font = Font(FONT_PATH, 128, self.text_color)
        self.title = Text(150, self.copyright1.y - title_font.size - 30, PROJECT_NAME, title_font)

        button_font = Font(FONT_PATH, 64, self.text_color)
        self.quit_button = Text(0, 0, '종료', button_font)
        self.quit_button.x = self.display.width - self.quit_button.surface.get_width() - 150
        self.quit_button.y = self.display.height - 150 - self.quit_button.font.size * 3 - 120
        self.quit_button_clickarea = ClickArea(
            self.mouse_manager, self.quit_button.surface.get_width(), self.quit_button.surface.get_height(),
            sticker=self.quit_button
        )

        self.place_button = Text(0, 0, '자리 선정', button_font)
        self.place_button.x = self.display.width - self.place_button.surface.get_width() - 150
        self.place_button.y = self.display.height - 150 - self.place_button.font.size * 2 - 60
        self.place_button_clickarea = ClickArea(
            self.mouse_manager, self.place_button.surface.get_width(), self.place_button.surface.get_height(),
            sticker=self.place_button
        )
        self.place_button_transition = Transition(RED_COLOR, self.display,
                                                  after=self._place_button_clickarea_transition_after)

        self.collocate_button = Text(0, 0, '자리 배치', button_font)
        self.collocate_button.x = self.display.width - self.collocate_button.surface.get_width() - 150
        self.collocate_button.y = self.display.height - 150 - self.collocate_button.font.size
        self.collocate_button_clickarea = ClickArea(
            self.mouse_manager, self.collocate_button.surface.get_width(), self.collocate_button.surface.get_height(),
            sticker=self.collocate_button
        )
        self.collocate_button_transition = Transition(IVORY_COLOR, self.display,
                                                      after=self._collocate_button_clickarea_transition_after)

        self.object_movers = (
            ObjectMover(self.title, initial_offset_x=-(150 + self.title.surface.get_width()) * 2),
            ObjectMover(self.copyright1, initial_offset_y=(150 + self.copyright1.surface.get_width()) * 2),
            ObjectMover(self.copyright2, initial_offset_y=(150 + self.copyright2.surface.get_width()) * 2),
            ObjectMover(self.quit_button, initial_offset_x=(150 + self.quit_button.surface.get_width()) * 2),
            ObjectMover(self.place_button, initial_offset_x=(150 + self.place_button.surface.get_width()) * 2),
            ObjectMover(self.collocate_button, initial_offset_x=(150 + self.collocate_button.surface.get_width()) * 2)
        )

    def tick(self):
        for object_mover in self.object_movers:
            object_mover.tick()

        self.quit_button_clickarea.tick()
        self.place_button_clickarea.tick()
        self.collocate_button_clickarea.tick()

        if self.quit_button_clickarea.clicked:
            self.shutdown()
        elif self.place_button_clickarea.clicked:
            self.place_button_transition.start()
        elif self.collocate_button_clickarea.clicked:
            self.collocate_button_transition.start()

        self.place_button_transition.tick()
        self.collocate_button_transition.tick()

    def _place_button_clickarea_transition_after(self):
        self.state_manager.set_state('place')

    def _collocate_button_clickarea_transition_after(self):
        self.state_manager.set_state('collocate')

    def render(self, surface: Surface):
        self.copyright1.render(surface)
        self.copyright2.render(surface)

        self.title.render(surface)

        self.quit_button.render(surface)
        self.place_button.render(surface)
        self.collocate_button.render(surface)

        self.place_button_transition.render(surface)
        self.collocate_button_transition.render(surface)
