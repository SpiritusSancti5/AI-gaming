from random import choice


def calculateMove(gameState):
    your_guesses = gameState["guesses"][gameState["PlayerIndex"]]

    two_letter_words = ["of", "to", "in", "it", "is"]

    for i in range(len(your_guesses)):
        print(len(your_guesses[i]))
        for j in range(len(your_guesses[i])):
            if your_guesses[i][j] == "":
                move = [i, j, choice(two_letter_words)]

                return move
    move = [-1, -1, "we"]

    return move
