import pygame
from main import *
from UIElement import UIElement
from GameState import GameState

# color we gonn are reuse
BLUE = (106, 159, 181)
BG_1 = (83, 228, 179)  # Mint Green
TXT_1 = (0, 0, 0)  # Black
PINK = (234, 208, 209)
WHITE = (255, 255, 255)

class FinishScreen:
    def __init__(self, screen):
        self.__screen = screen

    def run(self):  # to have our button, check main loop
        # start and quit button will be here
        back_btn = UIElement(
            center_position=(500, 470),
            font_size=30,
            bg_rgb=BG_1,
            text_rgb=TXT_1,
            text="Re-Start",
            action=GameState.NEWGAME,
        )
        quit_btn = UIElement(
            center_position=(500, 670),
            font_size=30,
            bg_rgb=BG_1,
            text_rgb=TXT_1,
            text="Quit",
            action=GameState.QUIT,
        )
        return_btn = UIElement(
            center_position=(500, 570),
            font_size=30,
            bg_rgb=BG_1,
            text_rgb=TXT_1,
            text="Back to main",
            action=GameState.TITLE,
        )

        buttons = [back_btn, return_btn, quit_btn]

        while True:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True
            self.__screen.fill(BG_1)  # re-draw the background

            for button in buttons:
                ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
                if ui_action is not None:
                    return ui_action
                button.draw(self.__screen)

            pygame.display.flip()
