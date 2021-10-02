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
FIN_BTN = (240, 150, 150)

finish_img = pygame.image.load('img/fail.png')
finish_img = pygame.transform.scale(finish_img, (1000, 800))

class FailedScreen:
    def __init__(self, screen):
        self.__screen = screen

    def run(self):  # to have our button, check main loop
        # start and quit button will be here
        back_btn = UIElement(
            center_position=(300, 600),
            font_size=30,
            bg_rgb=FIN_BTN,
            text_rgb=TXT_1,
            text="RETRY",
            action=GameState.NEWGAME,
        )

        return_btn = UIElement(
            center_position=(700, 600),
            font_size=30,
            bg_rgb=FIN_BTN,
            text_rgb=TXT_1,
            text="MENU",
            action=GameState.TITLE,
        )

        buttons = [back_btn, return_btn]


        while True:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True
            self.__screen.fill(BG_1)  # re-draw the background
            self.__screen.blit(finish_img, (0, 0))


            for button in buttons:
                ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
                if ui_action is not None:
                    return ui_action
                button.draw(self.__screen)


            pygame.display.flip()
