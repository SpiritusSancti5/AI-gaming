from random import choice


def calculateMove(gameState):
    path = []  # Initialise our path as an empty list
    starting_board = gameState['Board']  # Record our starting board
    cur_board = starting_board  # Record our current board as the starting board
    while not isValidSolution(cur_board):  # Keep looking until we find a solution
        if len(path) > 100:  # If our path gets too long, start again
            cur_board = starting_board  # Reset our current board to the starting board
            path = []  # Reset our path to the empty list
        potential_moves = getValidMoves(cur_board)  # Get the list of potential moves on the current board
        if path:  # If our path so far isn't empty
            potential_moves = [move for move in potential_moves if move != path[-1]]  # Remove the move that would undo the last move
        move = choice(potential_moves)  # Pick a random move
        path += [move]  # Add the move to our path

        cur_board = updateBoard(cur_board, move)  # Update our current board
    # We have found a solution
    return {"Steps": path}  # Return the solution


def isValidSolution(cur_board):  # Given a board returns whether it is solved or not
    k = 1  # Initialise correct tile value to 1
    for row in cur_board:  # For every row on the board
        for tile in row:  # For every tile in the row
            if tile != k:  # If the tile isn't the correct value
                return False  # Return board not solved
            k = (k + 1) % (len(cur_board)*len(cur_board[0]))  # Increment correct tile value
    return True  # Otherwise return board solved


def updateBoard(cur_board, move):  # Given a board and a move, returns an updated board with the move applied to it
    next_board = []  # Initialise the next board to the empty list
    for i in range(len(cur_board)):  # For every row on the board
        next_board.append([])  # Initialise the row element as an empty list
        for j in range(len(cur_board[i])):  # For every column on the board
            if cur_board[i][j] == move:  # If the current tile is equal to the one we moved
                next_board[i].append(0)  # That tile is now the blank tile
            elif cur_board[i][j] == 0:  # If the current tile is equal to the blank tile
                next_board[i].append(move)  # That tile is now the tile we moved
            else:  # Otherwise if the current tile wasn't involved in the move
                next_board[i].append(cur_board[i][j])  # Keep the tile the same
    return next_board  # Return the updated board


def getValidMoves(board):  # Find the potential moves that can be made from the given board configuration
    potential_moves = [board[i][j] for i in range(len(board)) for j in range(len(board[i]))
                       if (j + 1 < len(board[i]) and board[i][j + 1] == 0)  # Check left for blank
                       or (j > 0 and board[i][j - 1] == 0)  # Check right for blank
                       or (i + 1 < len(board) and board[i + 1][j] == 0)  # Check below for blank
                       or (i > 0 and board[i - 1][j] == 0)]  # Check above for blank
    return potential_moves  # Return all of the potential moves
