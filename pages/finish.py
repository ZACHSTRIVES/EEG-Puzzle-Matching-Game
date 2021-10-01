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

finish_img = pygame.image.load('img/finish_bg.png')
finish_img = pygame.transform.scale(finish_img, (1000, 800))


class FinishScreen:
    def __init__(self, screen):
        self.__screen = screen

    def run(self, total_time, attempts, correct, attention, total):  # to have our button, check main loop
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

        ft = pygame.font.SysFont('comicsansms', 15)
        ft2 = pygame.font.SysFont('comicsansms', 20)
        ft3 = pygame.font.SysFont('comicsansms', 20, True)
        txt1 = ft.render("TIME", True, TXT_1)
        txt2 = ft.render("ATTEMPTS", True, TXT_1)
        txt3 = ft.render("CORRECT", True, TXT_1)
        txt4 = ft.render("ATTENTION*", True, TXT_1)
        txt5 = ft2.render("TOTAL", True, TXT_1)

        txts = [[txt1, (260, 235)], [txt2, (560, 235)], [txt3, (260, 335)], [txt4, (560, 335)], [txt5, (260, 435)]]
        datas = [[str(total_time), (400, 235)], [str(attempts), (700, 235)], [str(correct)+"%", (400, 335)], [str(attention), (700, 335)], [str(total), (500, 435)]]

        while True:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True
            self.__screen.fill(BG_1)  # re-draw the background
            self.__screen.blit(finish_img, (0, 0))

            for txt in txts:
                self.__screen.blit(txt[0], txt[1])
            for data in datas:
                score = ft3.render(data[0], True, TXT_1)
                self.__screen.blit(score, data[1])
            notes = ft.render("*: The Average Attention Scores", True, TXT_1)
            self.__screen.blit(notes, (100, 680))

            for button in buttons:
                ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
                if ui_action is not None:
                    return ui_action
                button.draw(self.__screen)

            pygame.display.flip()
