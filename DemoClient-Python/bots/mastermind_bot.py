from random import randint


def calculateMove(gameState):  # TIP: For this game, you should really consider using the persistentData variable. (more info in the Programmer's Reference)
    print(gameState)  # Prints the input

    if gameState["Round"] == 0:  # Place pegs for other bot to guess
        if gameState["NumPegs"] == 4:  # If you need to give 4 pegs
            sequence = [1, 2, 0, 3]  # Don't use this, this is just an example
        else:  # If the number of pegs is not 4, create a random sequence for the other player to guess
            sequence = randomSequence(gameState["NumPegs"], gameState["NumColours"], gameState["DuplicatesAllowed"])
    else:  # Make a guess
        sequence = randomSequence(gameState["NumPegs"], gameState["NumColours"], gameState["DuplicatesAllowed"])  # random sequence
        # You can increase your chances by using the following script;
        # if ("Comparison" in gameState): # If you made a previous guess
        #    while compareGuess(sequence, gameState["GuessesList"][-1]) != gameState["Comparison"]: # Compare to your last guess
        #        sequence = randomSequence(gameState["NumPegs"], gameState["NumColours"], gameState["DuplicatesAllowed"])

    print('SEQUENCE: ' + str(sequence))  # Print your guess
    move = {  # This is the format you need to submit, changing this may result in an invalid move
        "Sequence": sequence
    }
    return move


# randomSequence: Get a random sequence
# pegs: The length of the sequence
# colours: The maximum value of a peg in the sequence
# duplicates: Whether a colour can be multiple times in the sequence
# Return: A random sequence that's in the defined bounds
# Examples:
# randomSequence(2, 4, False) CAN result in [1, 3] or [0, 1] or [3, 2] or ...
# randomSequence(2, 4, True)  CAN result in [1, 3] or [0, 0] or [2, 1] or ...
# randomSequence(2, 2, False) CAN result in [1, 0] or [0, 1]
def randomSequence(pegs, colours, duplicates):
    sequence = []
    for i in range(pegs):  # Loop the number of pebbles required
        rand = randint(0, colours - 1)
        if not duplicates:
            while rand in sequence:
                rand = randint(0, colours - 1)
        sequence.append(rand)  # Get a random colour and append it to the sequence
    return sequence


# compareGuess: Compares two sequences
# guess: The guess you want to compare
# sequence: The sequence that you want to compare the guess to
# Return: [the number of colours in the wrong place, the number of colours in the right place]
# Examples:
# compareGuess([0, 1, 0], [0, 2, 2]) will result in [0, 1]
# compareGuess([0, 1, 2], [2, 1, 0]) will result in [2, 1]
# compareGuess([0, 1, 0], [0, 1, 0]) will result in [0, 3]
def compareGuess(guess, sequence):
    sequence = sequence[:]  # create copies so we don't alter the originals
    guess = guess[:]  # create copies so we don't alter the originals
    comparison = [0, 0]  # initial result
    for i in range(len(guess)):  # find all correct ones
        if guess[i] == sequence[i]:  # if this is a correct colout at the correct place
            comparison[1] += 1  # add one to the correct counter
            sequence[i] = -1  # we used this peg
            guess[i] = -1  # we used this peg
    # find all the wrong placed correct ones, make sure you found the correct ones first
    for i in range(len(guess)):
        if guess[i] in sequence and not guess[i] == -1:  # if it is in the other sequence and is not used
            comparison[0] += 1  # add one to the wrong place counter
            sequence[sequence.index(guess[i])] = -1  # we used this peg
            guess[i] = -1  # we used this peg
    return comparison  # return the result
