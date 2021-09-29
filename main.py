import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from PyNeuro.PyNeuro import PyNeuro

#Import useful classes
from UIElement import UIElement
from GameState import GameState

#Import pages for game
from pages.game import *
from pages.info import *
from pages.finish import *
from pages.title import *


img = pygame.image.load("img/nosignal_v1.png")  # import img
img = pygame.transform.scale(img, (60, 60))
main_img = pygame.image.load('img/gameMain.png')
main_img = pygame.transform.scale(main_img, (260, 260))
logo = pygame.image.load("img/logo.png")
logo = pygame.transform.scale(logo, (32, 32))
rule = pygame.image.load("img/rule.png")
rule = pygame.transform.scale(rule, (633, 513))

# color we gonn are reuse
BLUE = (106, 159, 181)
BG_1 = (83, 228, 179)  # Mint Green
TXT_1 = (0, 0, 0)  # Black
PINK = (234, 208, 209)
WHITE = (255, 255, 255)


def main():
    pygame.init()
    pn = PyNeuro()
    pn.connect()
    pn.start()

    '''change: the size of main window and elememt position'''
    screen = pygame.display.set_mode((1000, 800))  # windows_size

    game_state = GameState.TITLE  # start with main(title) screen

    # set app name on top bar
    pygame.display.set_caption("EEG-Game")

    # set icon:
    pygame.display.set_icon(logo)

    while True:
        # The function below has move to independent def refere to different pages

        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.NEWGAME:
            game_state = play_level(screen)

        if game_state == GameState.FINISH:
            game_state = game_finish(screen)

        if game_state == GameState.INFO:
            game_state = game_info(screen)

        if game_state == GameState.QUIT:
            pygame.quit()
            return

# call main when the script is run
if __name__ == "__main__":
    main()
