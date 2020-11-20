
import arcade
import os
import board

DISK_MARGIN = 15
DISK_DIAMETER = 50
GAME_FOOTER = 100

GAME_WIDTH = board.BOARD_COLUMNS * \
    (DISK_MARGIN+1) + board.BOARD_COLUMNS*DISK_DIAMETER

GAME_HEIGHT = GAME_FOOTER + board.BOARD_ROWS * \
    (DISK_MARGIN+1) + board.BOARD_ROWS*DISK_DIAMETER

error = None


def drawBoard():
    radius = DISK_DIAMETER / 2
    y = GAME_HEIGHT - DISK_MARGIN - radius
    for row in board.board:
        x = DISK_MARGIN + radius
        for cell in row:

            # Draw fill if needed
            fillColor = None
            if cell == "R":
                fillColor = arcade.color.RED
            elif cell == "Y":
                fillColor = arcade.color.YELLOW
            if fillColor != None:
                arcade.draw_circle_filled(x, y, radius, fillColor)

            # Draw outline
            arcade.draw_circle_outline(x, y, radius, arcade.color.BLACK, 1)

            x += DISK_DIAMETER + DISK_MARGIN

        y -= DISK_DIAMETER + DISK_MARGIN


def drawMessage(message):
    arcade.draw_text(message, DISK_MARGIN, DISK_MARGIN, arcade.color.BLACK, 15)


def drawError(error):
    arcade.draw_text(error, DISK_MARGIN, 2 * DISK_MARGIN, arcade.color.RED, 15)


def getColumnFromX(posX: int) -> int:
    column = int((posX + DISK_MARGIN/2) / (DISK_DIAMETER + DISK_MARGIN))
    if column > board.BOARD_COLUMNS-1:
        column = board.BOARD_COLUMNS-1

    return column


# --------------------------------------------
# FOUR DISK WINDOWS
# --------------------------------------------
class FourDisksWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        # 1- Clear all
        arcade.start_render()

        # 2- Display board
        drawBoard()

        # 3- Display message on footer
        message = ""
        if board.getBoardStatus() == board.ON_GOING_STATUS:
            currentPlayer = board.getCurrentPlayer()
            message = "Player " + currentPlayer + ", click on a column to play"
            drawMessage(message)

        else:
            boardStatus = board.getBoardStatus()
            if boardStatus == board.RED_WON_STATUS:
                message = "Red player has won !"

            elif boardStatus == board.YELOW_WON_STATUS:
                message = "Yellow player has won !"
            else:
                message = "Draw game !"
        drawMessage(message)

        # 4- Draw error if any
        if error != None:
            drawError(error)

    def on_mouse_press(self, x, y, button, modifiers):
        global error
        error = None

        if button == arcade.MOUSE_BUTTON_LEFT:
            gameOnGoing = board.getBoardStatus() == board.ON_GOING_STATUS
            if gameOnGoing:
                # Get column from mouse positon
                column = getColumnFromX(x)

                if board.canPlay(column):
                    board.play(column)
                else:
                    error = "Cannot play on this column !"


# --------------------------------------------
# MAIN
# --------------------------------------------
FourDisksWindow(GAME_WIDTH, GAME_HEIGHT, "RONAN GAME")
arcade.run()
