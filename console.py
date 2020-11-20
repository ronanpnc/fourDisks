
import board


def printBoard():
    toPrint = ""
    for row in board.board:
        for cell in row:
            toPrint += str(cell) + " "
        toPrint += "\n"
    print(toPrint)


# The main programm on CONSOLE
while(board.getBoardStatus() == board.ON_GOING_STATUS):

    # 1- Display board
    printBoard()

    # 2- Ask user for column
    currentPlayer = board.getCurrentPlayer()
    diskColumn = int(input("Player " + currentPlayer + ", enter column: "))

    if board.canPlay(diskColumn):
        # Play the disk
        board.play(diskColumn)
    else:
        print("This column is full, try again")

boardStatus = board.getBoardStatus()

message = ""
if boardStatus == board.RED_WON_STATUS:
    message = "Red player has won !"

elif boardStatus == board.YELOW_WON_STATUS:
    message = "Yellow player has won !"
else:
    message = "Draw game !"

print(message)
