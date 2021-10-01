"""
@Author:: Zach Wang
This file provides the main game interface and the main game interface operation functions.
"""
from main import *
from Control import *
import random, pygame, sys
from pygame.locals import *
import statistics

# =======================================================================
# Score
HOLD_SECONDS = 4
ADD_SECONDS = 3
# =======================================================================

FPS = 30  # frames per second, the general speed of the program
WINDOWWIDTH = 1000  # size of window's width in pixels
WINDOWHEIGHT = 800  # size of windows' height in pixels
REVEALSPEED = 8  # speed boxes' sliding reveals and covers
BOXSIZE = 100  # size of box height & width in pixels
GAPSIZE = 10  # size of gap between boxes in pixels
BOARDWIDTH = 5  # number of columns of icons
BOARDHEIGHT = 4  # number of rows of icons
assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#            R    G    B
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
LIGHTBLUE = (106, 159, 181)

BGCOLOR = LIGHTBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS) * len(
    ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."

BACK_CARD = pygame.image.load("img/cards/backcard.png")
BACK_CARD = pygame.transform.scale(BACK_CARD, (BOXSIZE, BOXSIZE))

APPLE = pygame.transform.scale(pygame.image.load("img/cards/apple.png"), (BOXSIZE, BOXSIZE))
BANANA = pygame.transform.scale(pygame.image.load("img/cards/banana.png"), (BOXSIZE, BOXSIZE))
GRAPE = pygame.transform.scale(pygame.image.load("img/cards/grape.png"), (BOXSIZE, BOXSIZE))
ORANGE = pygame.transform.scale(pygame.image.load("img/cards/orange.png"), (BOXSIZE, BOXSIZE))
PEACH = pygame.transform.scale(pygame.image.load("img/cards/peach.png"), (BOXSIZE, BOXSIZE))
WATERMELON = pygame.transform.scale(pygame.image.load("img/cards/watermelon.png"), (BOXSIZE, BOXSIZE))
CHERRY = pygame.transform.scale(pygame.image.load("img/cards/cherry.jpg"), (BOXSIZE, BOXSIZE))
DRAGON = pygame.transform.scale(pygame.image.load("img/cards/dragon.png"), (BOXSIZE, BOXSIZE))
PINEAPPLE = pygame.transform.scale(pygame.image.load("img/cards/pineapple.png"), (BOXSIZE, BOXSIZE))
PEAR = pygame.transform.scale(pygame.image.load("img/cards/pear.png"), (BOXSIZE, BOXSIZE))
timer = pygame.image.load("img/clock.png")
timer = pygame.transform.scale(timer, (142, 88))
ADD3 = pygame.image.load("img/Add3.jpg")
ADD3 = pygame.transform.scale(ADD3, (60, 40))
ATTEMPS = pygame.image.load("img/attemps.png")
ATTEMPS = pygame.transform.scale(ATTEMPS, (113, 40))


class Game:

    def __init__(self, screen, finish):
        self.screen = screen
        self.__attention = 0
        self.__time = 60
        self.__currentTime = 0
        self.__secondsOverTemp = 0
        self.__showAdd = False
        self.__attemps = 0
        self.__wrong = 0
        self.__finishScreen = finish
        self.__attentionRecords = []

    @property
    def attention(self):
        return self.__attention

    @attention.setter
    def attention(self, value):
        self.__attention = value

    def play(self):
        global FPSCLOCK, DISPLAYSURF
        finsih_btn = UIElement(
            center_position=(140, 770),
            font_size=10,
            bg_rgb=BLUE,
            text_rgb=(0, 0, 0),
            text="Game finished",
            action=GameState.FINISH,
        )
        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

        mousex = 0  # used to store x coordinate of mouse event
        mousey = 0  # used to store y coordinate of mouse event
        pygame.display.set_caption('Memory Game')

        mainBoard = self.getRandomizedBoard()
        revealedBoxes = self.generateRevealedBoxesData(False)

        firstSelection = None  # stores the (x, y) of the first box clicked.

        DISPLAYSURF.fill(BGCOLOR)
        self.screen = DISPLAYSURF
        self.startGameAnimation(mainBoard)

        ATTENTION_BG = pygame.image.load("img/progress.png")
        ATTENTION_BG = pygame.transform.scale(ATTENTION_BG, (190, 40))
        ATTENTION_TEXT = pygame.image.load("img/attention.png")
        ATTENTION_TEXT = pygame.transform.scale(ATTENTION_TEXT, (113, 40))
        ATTENTION_WHITE_BAR = pygame.image.load("img/bar.png")

        start_ticks = pygame.time.get_ticks()  # starter tick

        while True:
            mouseClicked = False

            DISPLAYSURF.fill(BGCOLOR)  # drawing the window
            DISPLAYSURF.blit(ATTENTION_BG, (220, 100))
            DISPLAYSURF.blit(ATTENTION_TEXT, (100, 100))
            attention_bar_width = (self.attention / 100) * 190
            ATTENTION_WHITE_BAR = pygame.transform.scale(ATTENTION_WHITE_BAR, (int(attention_bar_width), 40))
            DISPLAYSURF.blit(ATTENTION_WHITE_BAR, (220, 100))
            self.drawBoard(mainBoard, revealedBoxes)
            DISPLAYSURF.blit(ATTEMPS, (470, 100))

            for event in pygame.event.get():  # event handling loop
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEMOTION:
                    mousex, mousey = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    mouseClicked = True

            self.seconds = int((pygame.time.get_ticks() - start_ticks) / 1000)  # calculate how many seconds

            if self.seconds != self.__currentTime:
                self.__attentionRecords.append(self.__attention)
                if self.attention > 60:
                    self.__secondsOverTemp += 1
                else:
                    self.__secondsOverTemp = 0

                if self.__secondsOverTemp == HOLD_SECONDS:
                    self.__time += ADD_SECONDS
                    self.__secondsOverTemp = 0
                    self.__showAdd = True
                else:
                    self.__showAdd = False
                if self.__showAdd:
                    self.screen.blit(ADD3, (900, 100))

                self.__currentTime = self.seconds
                self.__time -= 1

            clock_g = str(self.__time)

            textFont = pygame.font.SysFont('comicsansms', 25)
            TextSurf, TextReact = self.textObj(clock_g, textFont, WHITE)
            TextReact.center = (850, 100)
            DISPLAYSURF.blit(TextSurf, TextReact)
            DISPLAYSURF.blit(timer, (780, 57))

            boxx, boxy = self.getBoxAtPixel(mousex, mousey)
            if boxx != None and boxy != None:
                # The mouse is currently over a box.
                if not revealedBoxes[boxx][boxy]:
                    self.drawHighlightBox(boxx, boxy)
                if not revealedBoxes[boxx][boxy] and mouseClicked:
                    self.revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                    revealedBoxes[boxx][boxy] = True  # set the box as "revealed"
                    if firstSelection == None:  # the current box was the first box clicked
                        firstSelection = (boxx, boxy)
                    else:  # the current box was the second box clicked
                        # Check if there is a match between the two icons.
                        icon1shape = self.getShape(mainBoard, firstSelection[0], firstSelection[1])
                        icon2shape = self.getShape(mainBoard, boxx, boxy)

                        self.__attemps += 1

                        if icon1shape != icon2shape:
                            # Icons don't match. Re-cover up both selections.
                            pygame.time.wait(1000)  # 1000 milliseconds = 1 sec
                            self.coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                            revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                            revealedBoxes[boxx][boxy] = False
                            self.__wrong += 1
                        elif self.hasWon(revealedBoxes):  # check if all pairs found
                            self.endGame()
                        firstSelection = None  # reset firstSelection variable

            # Redraw the screen and wait a clock tick.
            pygame.display.update()
            FPSCLOCK.tick(FPS)

    def generateRevealedBoxesData(self, val):
        revealedBoxes = []
        for i in range(BOARDWIDTH):
            revealedBoxes.append([val] * BOARDHEIGHT)
        return revealedBoxes

    def getRandomizedBoard(self):
        # Get a list of every possible shape in every possible color.
        icons = [APPLE, BANANA, CHERRY, DRAGON, GRAPE, ORANGE, PEACH, PEAR, PINEAPPLE, WATERMELON]
        random.shuffle(icons)
        icons = icons[:10] * 2  # make two of each
        random.shuffle(icons)
        board = []
        for x in range(BOARDWIDTH):
            column = []
            for y in range(BOARDHEIGHT):
                column.append(icons[0])
                del icons[0]  # remove the icons as we assign them
            board.append(column)

        return board

    def splitIntoGroupsOf(self, groupSize, theList):
        # splits a list into a list of lists, where the inner lists have at
        # most groupSize number of items.
        result = []
        for i in range(0, len(theList), groupSize):
            result.append(theList[i:i + groupSize])
        return result

    def leftTopCoordsOfBox(self, boxx, boxy):
        # Convert board coordinates to pixel coordinates
        left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
        top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
        return (left, top)

    def getBoxAtPixel(self, x, y):
        for boxx in range(BOARDWIDTH):
            for boxy in range(BOARDHEIGHT):
                left, top = self.leftTopCoordsOfBox(boxx, boxy)
                boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
                if boxRect.collidepoint(x, y):
                    return (boxx, boxy)
        return (None, None)

    def drawIcon(self, shape, boxx, boxy):
        quarter = int(BOXSIZE * 0.25)  # syntactic sugar
        half = int(BOXSIZE * 0.5)  # syntactic sugar

        left, top = self.leftTopCoordsOfBox(boxx, boxy)  # get pixel coords from board coords
        # Draw the shapes
        self.screen.blit(shape, (left, top))

    def getShape(self, board, boxx, boxy):

        return board[boxx][boxy]

    def drawBoxCovers(self, board, boxes, coverage):
        # Draws boxes being covered/revealed. "boxes" is a list
        # of two-item lists, which have the x & y spot of the box.
        for box in boxes:
            left, top = self.leftTopCoordsOfBox(box[0], box[1])
            pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
            shape = self.getShape(board, box[0], box[1])
            self.drawIcon(shape, box[0], box[1])
            if coverage > 0:  # only draw the cover if there is an coverage
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

    def revealBoxesAnimation(self, board, boxesToReveal):
        # Do the "box reveal" animation.
        for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
            self.drawBoxCovers(board, boxesToReveal, coverage)

    def coverBoxesAnimation(self, board, boxesToCover):
        # Do the "box cover" animation.
        for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
            self.drawBoxCovers(board, boxesToCover, coverage)

    def drawBoard(self, board, revealed):
        # Draws all of the boxes in their covered or revealed state.
        for boxx in range(BOARDWIDTH):
            for boxy in range(BOARDHEIGHT):
                left, top = self.leftTopCoordsOfBox(boxx, boxy)
                if not revealed[boxx][boxy]:
                    # Draw a covered box.

                    self.screen.blit(BACK_CARD, (left, top))
                else:
                    # Draw the (revealed) icon.
                    shape = self.getShape(board, boxx, boxy)
                    self.drawIcon(shape, boxx, boxy)

    def drawHighlightBox(self, boxx, boxy):
        left, top = self.leftTopCoordsOfBox(boxx, boxy)
        pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)

    def startGameAnimation(self, board):
        # Randomly reveal the boxes 8 at a time.
        coveredBoxes = self.generateRevealedBoxesData(False)
        boxes = []
        for x in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT):
                boxes.append((x, y))
        random.shuffle(boxes)
        boxGroups = self.splitIntoGroupsOf(8, boxes)

        self.drawBoard(board, coveredBoxes)
        for boxGroup in boxGroups:
            self.revealBoxesAnimation(board, boxGroup)
            self.coverBoxesAnimation(board, boxGroup)

    def endGame(self):
        total_time = self.seconds
        attempts = self.__attemps
        print(self.__wrong,self.__attemps)
        rightRate = int((self.__attemps - self.__wrong) / self.__attemps * 100)
        attention = int(statistics.mean(self.__attentionRecords))
        total = int(rightRate + (int(self.__currentTime / total_time) * 60) + (attention * 0.8))
        self.__finishScreen.run(total_time, attempts, rightRate, attention, total)

    def hasWon(self, revealedBoxes):
        # Returns True if all the boxes have been revealed, otherwise False
        for i in revealedBoxes:
            if False in i:
                return False  # return False if any boxes are covered.
        return True

    def textObj(self, text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()
