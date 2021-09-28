import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from game import *

img = pygame.image.load("img/nosignal_v1.png") #import img
img = pygame.transform.scale(img, (60,60))
main_img = pygame.image.load('img/gameMain.png')
main_img = pygame.transform.scale(main_img, (260, 260))
logo = pygame.image.load("img/logo.png")
logo = pygame.transform.scale(logo, (32, 32))
rule = pygame.image.load("img/rule.png")
rule = pygame.transform.scale(rule, (633, 513))

#color we gonn are reuse
BLUE = (106, 159, 181)
BG_1 = (83, 228, 179) #Mint Green
TXT_1 = (0, 0, 0)#Black
PINK = (234, 208, 209)
WHITE = (255, 255, 255)


def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """ Returns surface with text written on """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()


class UIElement(Sprite):
    """ An user interface element that can be added to a surface """

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        """
        Args:
            center_position - tuple (x, y)
            text - string of text to write
            font_size - int
            bg_rgb (background colour) - tuple (r, g, b)
            text_rgb (text colour) - tuple (r, g, b)
        """
        self.mouse_over = False  # indicates if the mouse is over the element

        self.action = action

        # create the default image
        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        # create the image that shows when mouse is over the element
        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        # add both images and their rects to lists
        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        # calls the init method of the parent sprite class
        super().__init__()

    # properties that vary the image and its rect when the mouse is over the element
    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        """ Updates the element's appearance depending on the mouse position
            and returns the button's action if clicked.
        """
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        """ Draws element onto a surface """
        surface.blit(self.image, self.rect)

class GameState(Enum):
    QUIT = -1
    TITLE = 0 #main page
    NEWGAME = 1
    FINISH = 2
    INFO = 3

def main():
    pygame.init()

    '''change: the size of main window and elememt position'''
    screen = pygame.display.set_mode((1000, 800)) #windows_size

    game_state = GameState.TITLE #start with main(title) screen

    #set app name on top bar
    pygame.display.set_caption("EEG-Game")

    #set icon:
    pygame.display.set_icon(logo)

    # create a ui element
    # quit_btn = UIElement(
    #     center_position=(500, 650), #make sure our element will be center//The center right justfy 500 and top justify 700
    #     font_size=30,
    #     bg_rgb=BLUE,
    #     text_rgb=WHITE,
    #     text="Quit",
    #     action=GameState.QUIT,
    # )

    # main loop
    while True:
        #The function below has move to independent def refere to different pages
        '''
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BLUE)

        ui_action = quit_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return
        quit_btn.draw(screen)
        pygame.display.flip()
        '''

        if game_state == GameState.TITLE:
            game_state =  title_screen(screen)

        if game_state == GameState.NEWGAME:
            game_state = play_level(screen)

        if game_state == GameState.FINISH:
            game_state = game_finish(screen)

        if game_state == GameState.INFO:
            game_state = game_info(screen)

        if game_state == GameState.QUIT:
            pygame.quit()
            return

def title_screen(screen): #to have our button, check main loop
    #start and quit button will be here
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

    buttons = [start_btn, info_btn, quit_btn]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BG_1)#re-draw the background
        screen.blit(img, (930, 10))
        screen.blit(main_img, (370, 100))

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()

def play_level(screen):
    finsih_btn = UIElement(
        center_position=(140, 770),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=TXT_1,
        text="Game finished",
        action=GameState.FINISH,
    )

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BLUE)

        ui_action = finsih_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return ui_action
        finsih_btn.draw(screen)

        pygame.display.flip()

def game_finish(screen):
    return_btn = UIElement(
        center_position=(500, 500),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Game Over, Back to main page",
        action=GameState.TITLE,
    )

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BLUE)

        ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return ui_action
        return_btn.draw(screen)

        pygame.display.flip()

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

# call main when the script is run
if __name__ == "__main__":
    main()