# ----------------------------------------------
# CONSTANTS
# ----------------------------------------------
PLAYER_RED = "RED"
PLAYER_YELLOW = "YELLOW"

BOARD_ROWS = 6
BOARD_COLUMNS = 7

ON_GOING_STATUS = "ON_GOING_STATUS"
RED_WON_STATUS = "RED_WON_STATUS"
YELOW_WON_STATUS = "YELOW_WON_STATUS"
FULL_BOARD = "FULL_BOARD"


# We start with RED player !
currentPlayer = PLAYER_RED


def getNewBoard():
    return [["0"]*BOARD_COLUMNS for i in range(BOARD_ROWS)]


# We start with an empty grid !
board = getNewBoard()
currentBoardStatus = ON_GOING_STATUS

# We will keep the last position to compute the status of board
lastPlayPosition = None


# ----------------------------------------------
# PRIVATE FUNCTIONS
# ----------------------------------------------

def switchPlayer():
    global currentPlayer
    if currentPlayer == PLAYER_RED:
        currentPlayer = PLAYER_YELLOW
    else:
        currentPlayer = PLAYER_RED


def getDiskRowOn(diskColumn):
    for row in range(BOARD_ROWS-1, -1, -1):
        if board[row][diskColumn] == "0":
            return row
    return -1  # -1 means the  column is full !


def hasSameSign(positions):
    position = positions[0]
    firstSign = board[position[0]][position[1]]
    for position in positions:
        row = position[0]
        column = position[1]
        sign = board[row][column]
        if sign != firstSign:
            return False
    return True


def isInBoard(positions):
    for position in positions:
        row = position[0]
        column = position[1]
        if row < 0 or row >= BOARD_ROWS or column < 0 or column >= BOARD_COLUMNS:
            return False
    return True


def isBoardIsFull():
    for column in range(BOARD_COLUMNS):
        if board[0][column] == "0":
            return False
    return True


def getCombinationsFrom(row, column):
    combinations = [
        # vertical combinations
        [[row, column], [row+1, column], [row+2, column], [row+3, column]],
        [[row-1, column], [row, column], [row+1, column], [row+2, column]],
        [[row-2, column], [row-1, column], [row, column], [row+1, column]],
        [[row-3, column], [row-2, column], [row-1, column], [row, column]],

        # horizontal combinations
        [[row, column], [row, column+1], [row, column+2], [row, column+3]],
        [[row, column-1], [row, column], [row, column+1], [row, column+2]],
        [[row, column-2], [row, column-1], [row, column], [row, column+1]],
        [[row, column-3], [row, column-2], [row, column-1], [row, column]],

        # diagonal-asc combinations
        [[row, column], [row+1, column+1], [row+2, column+2], [row+3, column+3]],
        [[row-1, column-1], [row, column], [row+1, column+1], [row+2, column+2]],
        [[row-2, column-2], [row-1, column-1], [row, column], [row+1, column+1]],
        [[row-3, column-3], [row-2, column-2], [row-1, column-1], [row, column]],

        # diagonal-desc combinations
        [[row, column], [row+1, column-1], [row+2, column-2], [row+3, column-3]],
        [[row-1, column+1], [row, column], [row+1, column-1], [row+2, column-2]],
        [[row-2, column+2], [row-1, column+1], [row, column], [row+1, column-1]],
        [[row-3, column+3], [row-2, column+2], [row-1, column+1], [row, column]],
    ]
    return combinations


def computeBoardStatusFrom(row, column):
    if isBoardIsFull():
        return FULL_BOARD

    # Loop on all possible combivnations
    for combination in getCombinationsFrom(row, column):
        if isInBoard(combination) and hasSameSign(combination):
            if board[row][column] == "R":
                return RED_WON_STATUS
            else:
                return YELOW_WON_STATUS

    return ON_GOING_STATUS

# ----------------------------------------------
# PUBLIC API
# ----------------------------------------------


def getCurrentPlayer():
    return currentPlayer


def getBoardStatus():
    return currentBoardStatus


def canPlay(diskColumn):
    return getDiskRowOn(diskColumn) != -1


def play(diskColumn):
    # 1- Get the corresponding disk row
    # We assume it's not -1 due to game play
    diskRow = getDiskRowOn(diskColumn)

    # 2- Update the board at this row/column
    global board

    if currentPlayer == PLAYER_RED:
        diskSign = "R"
    else:
        diskSign = "Y"

    board[diskRow][diskColumn] = diskSign

    # 4- Update board status
    global currentBoardStatus
    currentBoardStatus = computeBoardStatusFrom(diskRow, diskColumn)

    # 3- Switch player
    switchPlayer()
