from enum import Enum

class GameState(Enum):
    QUIT = -1
    TITLE = 0  # main page
    FINISH = 1
    NEWGAME = 2
    INFO = 3
    FAIL = 4