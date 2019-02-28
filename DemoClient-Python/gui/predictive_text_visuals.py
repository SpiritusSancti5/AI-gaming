import tkinter

ASSETS_PATH = 'assets/56'

TABLE_WIDTH = 360
TABLE_HEIGHT = 360
TABLE_COLOUR = '#DDDDDD'
TABLE_BORDER = 1


class PredictiveTextVisuals(tkinter.Canvas):
    def __init__(self, root):
        super().__init__(root, width=TABLE_WIDTH, height=TABLE_HEIGHT, bg=TABLE_COLOUR, bd=TABLE_BORDER)
        self.myBoard = None
        self.oppBoard = None
        self.gameText = tkinter.Text(self, height=20, width=35)
        self.gameText.grid(row=2, column=0, columnspan=1, rowspan=10, pady=(4, 0))
        self.gameText.insert("1.0", "None")

    def draw_board(self, gamestate, my_board):
        output = ""
        if my_board:
            for i in range(len(gamestate["Redacted"])):
                output += str(i + 1) + '. ' + guess(gamestate["Redacted"][i], gamestate["guesses"][0][i])
                output += "\n"
            output += "\n\n\n"
            self.gameText.insert("1.0", output)
        else:
            for i in range(len(gamestate["Redacted"])):
                output += str(i + 1) + '. ' + guess(gamestate["Redacted"][i], gamestate["guesses"][1][i])
                output += "\n"
            output += "\n\n\n"
            self.gameText.insert("1.0", output)

    def clear_board(self):
        self.gameText.delete("1.0", tkinter.END)
        self.gameText.insert("1.0", "None")

    def draw_game_state(self, game_state, my_board):
        if my_board:
            self.draw_board(game_state, my_board)
        else:
            self.draw_board(game_state, my_board)


def guess(sentence, guesses):
    guesses = [i if i != "" else "__" for i in guesses]
    guessed_sentence = ''  # Sentence so far
    count = 0  # Number of guesses used so far
    for word in sentence:  # For every word in the sentence
        if word == '__':  # If the word is a blank
            # Fill in blank with current guess word
            guessed_sentence += guesses[count] + ' '
            count += 1  # Increment current guess word
        elif len(word) == 2:  # Implies switched word game
            if guesses[count] == '__':  # If current guess is two blanks
                guessed_sentence += word + ' '  # Add next word to the sentence
            else:  # If current guess is not blank
                # Add guess to the sentence
                guessed_sentence += guesses[count] + ' '
            count += 1  # Increment current guess word
        else:  # If normal word in the sentence
            guessed_sentence += word + ' '  # Add next word to the sentence
    return guessed_sentence
