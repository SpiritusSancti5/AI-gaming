import time
import random
import json
from random import randint, choice
from copy import deepcopy
import requests
from bots.mover import persistentData


def calculateMove(gamestate):
    # Retrieving gamestate values
    move 	= [[], []]
    board   = gamestate["Board"]
    max_rows, max_columns = len(board) - 1, len(board[0]) - 1  # maximal row and column indices
    hand    = gamestate["MyHand"]
    scoring = gamestate["TileScores"]

    # Setting up a checker to determine if the bot passed in the previous turn
    if persistentData == {}:
        persistentData["PassedLastTurn"] = False

    # Finding the occupied places:
    occupied = []
    for column in range(max_columns + 1):
        for row in range(max_rows + 1):
            if board[row][column] != ' ':
                occupied.append([row, column])

    fullDictwords = dictionary_retrieval(gamestate["Dictionary"])

    # Finding a valid word
    scoringword   = [[], [], [], None]  # [[Word],[Starting position],[Axis],index of the tile already on the board]

    middle_row    = int(max_rows / 2)
    middle_column = int(max_columns / 2)
    if board[middle_row][middle_column] != ' ':  # If it's not the first go
        while scoringword[0] == [] and gamestate["ResponseDeadline"] - int(time.time() * 1000) > 2000:

            occupied_cell = random.choice(occupied)
            row = occupied_cell[0]
            column = occupied_cell[1]

            print("chosen cell: " +  str(occupied_cell) + ", letter " + str(board[row][column]))

            # Determining the axis of the word that includes it:
            if (0 < row < max_rows and board[row + 1][column] == ' ' and board[row - 1][column] == ' ') or (
                row == 0 and board[row + 1][column] == ' ') or (row == max_rows and board[row - 1][column] == ' '):
                axis = 'H'
            elif (0 < column < max_rows and board[row][column + 1] == ' ' and board[row][column - 1] == ' ') or (
                  column == 0 and board[row][column + 1] == ' ') or (column == max_columns and board[row][column - 1] == ' '):
                axis = 'V'
            else:
                continue # find another occupied cell

            if axis == 'H':
                axismove = [-1, 0]
            elif axis == 'V':
                axismove = [0, 1]

            print("axis: " + axis)

            # Find the available intervals for a new word
            spaceback = 0
            spaceforw = 0
            while (0 <= row + (spaceback + 1) * axismove[0] <= max_rows and
                   0 <= column + (spaceback + 1) * axismove[1] <= max_columns and
                   board[row + (spaceback + 1) * axismove[0]][column + (spaceback + 1) * axismove[1]] == ' '):
                spaceback += 1
            while (0 <= row - (spaceforw + 1) * axismove[0] <= max_rows and 0 <= column - (spaceforw + 1) * axismove[1] <= max_columns
				   and board[row - (spaceforw + 1) * axismove[0]][column - (spaceforw + 1) * axismove[1]] == ' '):
                spaceforw += 1
            if spaceback > 0:
                spaceback -= 1
            if spaceforw > 0:
                spaceforw -= 1

            # Find words that fit into that interval
            dictwords = findDictWords(board[row][column], spaceback, spaceforw, fullDictwords, gamestate)
            for word in dictwords:
                if scoringword[0] != []:
                    break
                else:
                    if checkHand(word, hand): # can this word be built using the hand
                        starting_position = getStartingPosition(board[row][column], word, axismove, row, column)
                        scoringword = [list(word), starting_position, axismove, word.index(board[row][column])]
                        print("scoringword: " + str(scoringword))

    else:  # If it is the first turn
        for word in fullDictwords:
            if gamestate["ResponseDeadline"] - int(time.time() * 1000) > 2000:
                if len(word) >= 3:
                    temphand = deepcopy(hand)
                    detachedword = list(word)
                    for letter in detachedword:
                        if letter not in temphand:
                            break
                        else:
                            temphand.remove(letter)
                    else:
                        scoringword[0] = detachedword
                        scoringword[1] = [middle_row, middle_column]
                        scoringword[2] = [1, 0]


    # If we cannot find any words:
    if scoringword[0] == []:
        if gamestate["FirstGo"] == True or gamestate["NumberOfTilesInBag"] < 7 or persistentData["PassedLastTurn"] == True:
            move[1] = ['Pass']
        else:
            # Exchange Tiles:
            number_exchanged = randint(0, len(hand))
            for x in range(0, number_exchanged):
                move[0].append(gamestate["MyHand"][x])
            move[1] = ['Pass']
        persistentData["PassedLastTurn"] = True
    else:
        # If we found a word, create the move output
        move[0] = scoringword[0]
        start = scoringword[1]
        axismove = scoringword[2]

        for i in range(len(move[0])):
            position = [start[1] + i*axismove[1], start[0] + i*axismove[0]]
            move[1].append(position)

        # If we used a tile on the board, remove it from the move output
        usedindex = scoringword[3]
        if usedindex != None:
            move[0].pop(usedindex)
            move[1].pop(usedindex)
        persistentData["PassedLastTurn"] = False
    print("My move is:" + str(move))
    return move


# Finds all words that can be put  in a particular position on the board
def findDictWords(letter, spaceback, spaceforw, fullDictwords, gamestate):
    dictwords = []
    for word in fullDictwords:
        if gamestate["ResponseDeadline"] - int(time.time() * 1000) < 2000:
            break
        else:
            if len(word) > 2 and (letter in word) and (len(word) <= spaceback + spaceforw + 1):
                index = word.index(letter)
                first_segment = word[:index]
                second_segment = word[index+1:]
                if len(first_segment) <= spaceforw and len(second_segment) <= spaceback:
                    dictwords.append(word)
    return dictwords


# Calculates the starting cell of the chosen word
def getStartingPosition(letter, word, axismove, row, column):
    index = word.index(letter)
    starting_position = [row - (index*axismove[0]), column - (index*axismove[1])]
    return starting_position


# Checks whether a word can be composed using the hand
def checkHand(word, hand):
    temphand = deepcopy(hand)
    detachedword = list(word)
    for letter in detachedword:
        if letter not in temphand:
            return False
        else:
            temphand.remove(letter)
    return True


# Returns a list of all words from the dictionary
def dictionary_retrieval(Dictionary):
    r = requests.get(Dictionary)
    dictwordsoriginal = r.text.strip().upper()
    dictwords = dictwordsoriginal.split(' ')
    return dictwords