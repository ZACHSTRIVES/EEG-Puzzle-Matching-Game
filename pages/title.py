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

noSignal = pygame.image.load("img/nosignal_v1.png")  # import img
noSignal = pygame.transform.scale(noSignal, (60, 60))

connected = pygame.image.load("img/connected_v1.png")
connected = pygame.transform.scale(connected, (60, 60))

connecting_1 = pygame.image.load("img/connecting1_v1.png")
connecting_1 = pygame.transform.scale(connecting_1, (60, 60))

connecting_2 = pygame.image.load("img/connecting3_v1.png")
connecting_2 = pygame.transform.scale(connecting_2, (60, 60))

main_img = pygame.image.load('img/gameMain.png')
main_img = pygame.transform.scale(main_img, (260, 260))


class TitleScreen:

    def __init__(self, screen):
        self.__screen = screen
        self.__signal_status = "NotConnected"

    @property
    def signal_status(self):
        return self.__signal_status

    @signal_status.setter
    def signal_status(self, status):
        self.__signal_status = status

    def run(self):
        start_btn = UIElement(
            center_position=(500, 470),
            font_size=40,
            bg_rgb=BG_1,
            text_rgb=TXT_1,
            text="Start",
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
        info_btn = UIElement(
            center_position=(500, 570),
            font_size=30,
            bg_rgb=BG_1,
            text_rgb=TXT_1,
            text="How to play",
            action=GameState.INFO,
        )
        test_btn = UIElement(
            center_position=(500, 0),
            font_size=30,
            bg_rgb=BG_1,
            text_rgb=TXT_1,
            text="test",
            action=GameState.FINISH,
        )

        buttons = [test_btn, start_btn, info_btn, quit_btn]

        while True:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True

            self.__screen.fill(BG_1)  # re-draw the background
            self.__screen.blit(main_img, (370, 100))
            if self.signal_status == "scanning":
                self.__screen.blit(connecting_1, (930, 10))
            elif self.signal_status == "fitting":
                self.__screen.blit(connecting_2, (930, 10))
            elif self.signal_status == "connected":
                self.__screen.blit(connected, (930, 10))
            else:
                self.__screen.blit(noSignal, (930, 10))

            for button in buttons:
                ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
                if ui_action is not None:
                    return ui_action
                button.draw(self.__screen)

            pygame.display.flip()



