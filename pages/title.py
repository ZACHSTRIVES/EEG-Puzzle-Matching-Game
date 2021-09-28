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

img = pygame.image.load("img/nosignal_v1.png")  # import img
img = pygame.transform.scale(img, (60, 60))
main_img = pygame.image.load('img/gameMain.png')
main_img = pygame.transform.scale(main_img, (260, 260))


def title_screen(screen):  # to have our button, check main loop
    # start and quit button will be here
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
        screen.fill(BG_1)  # re-draw the background
        screen.blit(img, (930, 10))
        screen.blit(main_img, (370, 100))

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()