from random import randint


def calculateMove(gameState):
    ret = dict()
    pos = randomGuesser(gameState)
    print('My move is '+str(pos)+' OpponentId: '+gameState['OpponentId'])
    ret['Position'] = pos
    return ret


def randomGuesser(gamestate):  # Randomly guesses a position
    move = randint(0, 8)  # Random guess
    while gamestate["Board"][move] != " ":  # If taken...
        move = randint(0, 8)  # ... keep random guessing until found one
    return move


def oppTwoInRow(gamestate):  # Returns the (first) location that will block your opponent from winning, returns -1 otherwise
    myRole = gamestate["Role"]
    if myRole == "X":
        oppRole = "O"
    else:
        oppRole = "X"
    if((gamestate["Board"][1] == oppRole and gamestate["Board"][2] == oppRole)or(gamestate["Board"][3] == oppRole and gamestate["Board"][6] == oppRole)or(gamestate["Board"][4] == oppRole and gamestate["Board"][8] == oppRole))and gamestate["Board"][0] == " ":
        move = 0
    elif((gamestate["Board"][0] == oppRole and gamestate["Board"][2] == oppRole)or(gamestate["Board"][4] == oppRole and gamestate["Board"][7] == oppRole))and gamestate["Board"][1] == " ":
        move = 1
    elif((gamestate["Board"][0] == oppRole and gamestate["Board"][1] == oppRole)or(gamestate["Board"][4] == oppRole and gamestate["Board"][6] == oppRole)or(gamestate["Board"][5] == oppRole and gamestate["Board"][8] == oppRole))and gamestate["Board"][2] == " ":
        move = 2
    elif((gamestate["Board"][0] == oppRole and gamestate["Board"][6] == oppRole)or(gamestate["Board"][4] == oppRole and gamestate["Board"][5] == oppRole))and gamestate["Board"][3] == " ":
        move = 3
    elif((gamestate["Board"][0] == oppRole and gamestate["Board"][8] == oppRole)or(gamestate["Board"][1] == oppRole and gamestate["Board"][7] == oppRole)or(gamestate["Board"][2] == oppRole and gamestate["Board"][6] == oppRole)or(gamestate["Board"][3] == oppRole and gamestate["Board"][5] == oppRole))and gamestate["Board"][4] == " ":
        move = 4
    elif((gamestate["Board"][2] == oppRole and gamestate["Board"][8] == oppRole)or(gamestate["Board"][3] == oppRole and gamestate["Board"][4] == oppRole))and gamestate["Board"][5] == " ":
        move = 5
    elif((gamestate["Board"][0] == oppRole and gamestate["Board"][3] == oppRole)or(gamestate["Board"][2] == oppRole and gamestate["Board"][4] == oppRole)or(gamestate["Board"][7] == oppRole and gamestate["Board"][8] == oppRole))and gamestate["Board"][6] == " ":
        move = 6
    elif((gamestate["Board"][1] == oppRole and gamestate["Board"][4] == oppRole)or(gamestate["Board"][6] == oppRole and gamestate["Board"][8] == oppRole))and gamestate["Board"][7] == " ":
        move = 7
    elif((gamestate["Board"][0] == oppRole and gamestate["Board"][4] == oppRole)or(gamestate["Board"][2] == oppRole and gamestate["Board"][5] == oppRole)or(gamestate["Board"][6] == oppRole and gamestate["Board"][7] == oppRole))and gamestate["Board"][8] == " ":
        move = 8
    else:
        move = -1
    return move


def twoInRow(gamestate):  # Returns the (first) location that will give you three in a row, returns -1 if none exist
    myRole = gamestate["Role"]
    if((gamestate["Board"][1] == myRole and gamestate["Board"][2] == myRole)or(gamestate["Board"][3] == myRole and gamestate["Board"][6] == myRole)or(gamestate["Board"][4] == myRole and gamestate["Board"][8] == myRole))and gamestate["Board"][0] == " ":
        move = 0
    elif((gamestate["Board"][0] == myRole and gamestate["Board"][2] == myRole)or(gamestate["Board"][4] == myRole and gamestate["Board"][7] == myRole))and gamestate["Board"][1] == " ":
        move = 1
    elif((gamestate["Board"][0] == myRole and gamestate["Board"][1] == myRole)or(gamestate["Board"][4] == myRole and gamestate["Board"][6] == myRole)or(gamestate["Board"][5] == myRole and gamestate["Board"][8] == myRole))and gamestate["Board"][2] == " ":
        move = 2
    elif((gamestate["Board"][0] == myRole and gamestate["Board"][6] == myRole)or(gamestate["Board"][4] == myRole and gamestate["Board"][5] == myRole))and gamestate["Board"][3] == " ":
        move = 3
    elif((gamestate["Board"][0] == myRole and gamestate["Board"][8] == myRole)or(gamestate["Board"][1] == myRole and gamestate["Board"][7] == myRole)or(gamestate["Board"][2] == myRole and gamestate["Board"][6] == myRole)or(gamestate["Board"][3] == myRole and gamestate["Board"][5] == myRole))and gamestate["Board"][4] == " ":
        move = 4
    elif((gamestate["Board"][2] == myRole and gamestate["Board"][8] == myRole)or(gamestate["Board"][3] == myRole and gamestate["Board"][4] == myRole))and gamestate["Board"][5] == " ":
        move = 5
    elif((gamestate["Board"][0] == myRole and gamestate["Board"][3] == myRole)or(gamestate["Board"][2] == myRole and gamestate["Board"][4] == myRole)or(gamestate["Board"][7] == myRole and gamestate["Board"][8] == myRole))and gamestate["Board"][6] == " ":
        move = 6
    elif((gamestate["Board"][1] == myRole and gamestate["Board"][4] == myRole)or(gamestate["Board"][6] == myRole and gamestate["Board"][8] == myRole))and gamestate["Board"][7] == " ":
        move = 7
    elif((gamestate["Board"][0] == myRole and gamestate["Board"][4] == myRole)or(gamestate["Board"][2] == myRole and gamestate["Board"][5] == myRole)or(gamestate["Board"][6] == myRole and gamestate["Board"][7] == myRole))and gamestate["Board"][8] == " ":
        move = 8
    else:
        move = -1
    return move
