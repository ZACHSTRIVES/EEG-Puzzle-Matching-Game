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

rule = pygame.image.load("img/rule.png")
rule = pygame.transform.scale(rule, (633, 513))

def game_info(screen):
    info_btn = UIElement(
        center_position=(500, 700),
        font_size=30,
        bg_rgb=PINK,
        text_rgb=TXT_1,
        text="Back to main",
        action=GameState.TITLE,
    )

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(PINK)

        ui_action = info_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return ui_action
        info_btn.draw(screen)
        screen.blit(rule, (193, 80))

        pygame.display.flip()