from random import choice
import json


# These are the only additional libraries available to you. Uncomment them
# to use them in your solution.
#
# import numpy    # Base N-dimensional array package
# import pandas   # Data structures & analysis

# =============================================================================
# This calculateMove() function is where you need to write your code. When it
# is first loaded, it will play a complete game for you using the Helper
# functions that are defined below. The Helper functions give great example
# code that shows you how to manipulate the data you receive and the move
# that you have to return.
#

def calculateMove(gameState):
    print(gameState)

    # The key value pair "PossibleMoves" stores a list of all the valid moves
    # you can make during this turn in the form [row, column]
    possible_moves = gameState["PossibleMoves"]

    # We will choose a random move
    move = choice(possible_moves)

    # Now we submit that move in the correct JSON format
    return {"Row": move[0], "Column": move[1]}
