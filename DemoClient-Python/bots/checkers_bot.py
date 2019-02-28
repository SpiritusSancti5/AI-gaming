from random import choice
from json import loads


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

def calculateMove(gamestate):
    print(gamestate)

    # Choose a random key-value pair from the possible moves
    move_from, move_to = choice(list(gamestate["PossibleMoves"].items()))
    # Convert key string to coordinates of checker to move
    move_from = loads(move_from)
    # Choose a random possible set of coordinates for the checker to move to
    move_to = choice(move_to)
    # Print the move
    print(move_from, move_to)
    # Return the move
    return {"From": move_from, "To": [move_to]}
