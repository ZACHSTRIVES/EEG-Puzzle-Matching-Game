from enum import Enum

class GameState(Enum):
    QUIT = -1
    TITLE = 0  # main page
    NEWGAME = 1
    FINISH = 2
    INFO = 3
    FAIL = 4