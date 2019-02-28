from random import randint


def calculateMove(gameState):

    # When manipulating the Board remember the positions are as follows
    #
    # 0| -   -   -   -   -   -   -
    # 1| -   -   -   -   -   -   -
    # 2| -   -   -   -   -   -   -
    # 3| -   R   R   Y   Y   -   -
    # 4| -   Y   R   R   R   -   -
    # 5| Y   R   R   Y   Y   -   Y
    # ----------------------------
    #    0   1   2   3   4   5   6
    #
    #
    # 0|-1  -1  -1  -1  -1  -1  -1
    # 1|-1  -1  -1  -1  -1  -1  -1
    # 2|-1  -1  -1  -1  -1  -1  -1
    # 3|-1   1   1   0   0  -1  -1
    # 4|-1   0   1   1   1  -1  -1
    # 5| 0   1   1   0   0  -1   0
    # ----------------------------
    #    0   1   2   3   4   5   6
    #
    # -1 - Empty space
    #  0 - Your disc in this case yellow (Y)
    #  1 - Your opponents disc red (R)

    # print(gameState["Board"])

    # Makes a random drop in any column that is not full
    dropColumn = randint(0, len(gameState["Board"][0])-1)
    while isColumnFullX(dropColumn, gameState["Board"]):
        dropColumn = randint(0, len(gameState["Board"][0])-1)

    return {"Column": dropColumn}


def isColumnFullX(dropColumn, board):
    # Check the top row has an empty space
    if board[0][dropColumn] == -1:
        return False

    return True
