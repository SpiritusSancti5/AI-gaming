from time import sleep
from random import choice


def calculateMove(gameState):
    sleep(2)

    # Example of a move, this will not solve the cube
    moves = ["1R", "1U", "1D", "1L", "1F", "1F", "1B", "1R'", "1U'", "1D'", "1U", "1D", "1L'", "1F'", "1B'"]

    return {"Turns": moves}


def randomMove():
    move = choice(["1R", "1U", "1D", "1L", "1F", "1B", "1R'", "1U'", "1D'", "1L'", "1F'", "1B'"])
    return move


def isSolved(board):
    for f in ["FRONT", "BACK", "LEFT", "RIGHT", "UP", "DOWN"]:
        face = board[f]
        for row in range(len(face)):
            for col in range(len(face)):
                if face[row][col][0] != face[0][0][0]:
                    return False
    return True


def makeMove(move, board):
    for m in move["Turns"]:
        makeTurn(board, m)


# Decomposes a given turn into a 'twist' and a 'rotate' (see below) and runs both functions
def makeTurn(cube, turn):

    oppositeFaces = {"F": "B", "B": "F", "R": "L", "L": "R", "U": "D", "D": "U"}
    fullFaces = {"F": "FRONT", "B": "BACK", "R": "RIGHT", "L": "LEFT", "U": "UP", "D": "DOWN"}
    cubeSize = len(cube["FRONT"])

    depth = int(turn[0])
    face = turn[1]

    if len(turn) == 3:
        twist(cube, oppositeFaces[face], cubeSize - depth + 1)
    else:
        twist(cube, face, depth)

    if depth == 1:
        if len(turn) == 3:
            rotate(cube[fullFaces[face]], "ANTICLOCKWISE")
        else:
            rotate(cube[fullFaces[face]], "CLOCKWISE")
    elif depth == cubeSize:
        # Rotating a face on the opposite side of the cube means you rotate it the other way
        if len(turn) == 3:
            rotate(cube[fullFaces[oppositeFaces[face]]], "CLOCKWISE")
        else:
            rotate(cube[fullFaces[oppositeFaces[face]]], "ANTICLOCKWISE")


# Rotates colours on one of the cube's faces, without changing the colours on the blocks' edges
def rotate(cubeFace, direction):
    cubeSize = len(cubeFace)
    if direction == "CLOCKWISE":
        for i in range(cubeSize // 2):
            for j in range(i, cubeSize - i - 1):
                temp = cubeFace[i][j]
                cubeFace[i][j] = cubeFace[cubeSize - j - 1][i]
                cubeFace[cubeSize - j - 1][i] = cubeFace[cubeSize - i - 1][cubeSize - j - 1]
                cubeFace[cubeSize - i - 1][cubeSize - j - 1] = cubeFace[j][cubeSize - i - 1]
                cubeFace[j][cubeSize - i - 1] = temp
    else:
        for i in range(cubeSize // 2):
            for j in range(i, cubeSize - i - 1):
                temp = cubeFace[j][i]
                cubeFace[j][i] = cubeFace[i][cubeSize - j - 1]
                cubeFace[i][cubeSize - j - 1] = cubeFace[cubeSize - j - 1][cubeSize - i - 1]
                cubeFace[cubeSize - j - 1][cubeSize - i - 1] = cubeFace[cubeSize - i - 1][j]
                cubeFace[cubeSize - i - 1][j] = temp


# Twists the edges around a slice of blocks clockwise
def twist(cube, face, depth):
    cubeSize = len(cube["FRONT"])
    if face == "F":
        for i in range(cubeSize):
            temp = cube["UP"][cubeSize - depth][i]
            cube["UP"][cubeSize - depth][i] = cube["LEFT"][cubeSize - i - 1][cubeSize - depth]
            cube["LEFT"][cubeSize - i - 1][cubeSize - depth] = cube["DOWN"][depth - 1][cubeSize - i - 1]
            cube["DOWN"][depth - 1][cubeSize - i - 1] = cube["RIGHT"][i][depth - 1]
            cube["RIGHT"][i][depth - 1] = temp

    elif face == "B":
        for i in range(cubeSize):
            temp = cube["UP"][depth - 1][cubeSize - i - 1]
            cube["UP"][depth - 1][cubeSize - i - 1] = cube["RIGHT"][cubeSize - i - 1][cubeSize - depth]
            cube["RIGHT"][cubeSize - i - 1][cubeSize - depth] = cube["DOWN"][cubeSize - depth][i]
            cube["DOWN"][cubeSize - depth][i] = cube["LEFT"][i][depth - 1]
            cube["LEFT"][i][depth - 1] = temp

    elif face == "L":
        for i in range(cubeSize):
            temp = cube["UP"][i][depth - 1]
            cube["UP"][i][depth - 1] = cube["BACK"][cubeSize - i - 1][cubeSize - depth]
            cube["BACK"][cubeSize - i - 1][cubeSize - depth] = cube["DOWN"][i][depth - 1]
            cube["DOWN"][i][depth - 1] = cube["FRONT"][i][depth - 1]
            cube["FRONT"][i][depth - 1] = temp

    elif face == "R":
        for i in range(cubeSize):
            temp = cube["UP"][cubeSize - i - 1][cubeSize - depth]
            cube["UP"][cubeSize - i - 1][cubeSize - depth] = cube["FRONT"][cubeSize - i - 1][cubeSize - depth]
            cube["FRONT"][cubeSize - i - 1][cubeSize - depth] = cube["DOWN"][cubeSize - i - 1][cubeSize - depth]
            cube["DOWN"][cubeSize - i - 1][cubeSize - depth] = cube["BACK"][i][depth - 1]
            cube["BACK"][i][depth - 1] = temp

    elif face == "U":
        for i in range(cubeSize):
            temp = cube["BACK"][depth - 1][cubeSize - i - 1]
            cube["BACK"][depth - 1][cubeSize - i - 1] = cube["LEFT"][depth - 1][cubeSize - i - 1]
            cube["LEFT"][depth - 1][cubeSize - i - 1] = cube["FRONT"][depth - 1][cubeSize - i - 1]
            cube["FRONT"][depth - 1][cubeSize - i - 1] = cube["RIGHT"][depth - 1][cubeSize - i - 1]
            cube["RIGHT"][depth - 1][cubeSize - i - 1] = temp

    else:
        for i in range(cubeSize):
            temp = cube["FRONT"][cubeSize - depth][i]
            cube["FRONT"][cubeSize - depth][i] = cube["LEFT"][cubeSize - depth][i]
            cube["LEFT"][cubeSize - depth][i] = cube["BACK"][cubeSize - depth][i]
            cube["BACK"][cubeSize - depth][i] = cube["RIGHT"][cubeSize - depth][i]
            cube["RIGHT"][cubeSize - depth][i] = temp
