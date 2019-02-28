from random import randint


def calculateMove(gameState):
    boardWidth = len(gameState["Board"])    # Number of columns of intersections
    boardHeight = len(gameState["Board"][0])    # Number of rows of intersections
    return {"X": randint(0, boardWidth - 1),    # Select a random x co-ordinate to place a stone
            "Y": randint(0, boardHeight - 1)}   # Select a random y co-ordinate to place a stone
