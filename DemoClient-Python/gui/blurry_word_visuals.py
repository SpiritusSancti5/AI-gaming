import tkinter

ASSETS_PATH = 'assets/59'

TABLE_WIDTH = 360
TABLE_HEIGHT = 360
TABLE_COLOUR = '#DDDDDD'
TABLE_BORDER = 1


class MicrosoftCognitiveChallengeVisuals(tkinter.Canvas):
    def __init__(self, root):
        super().__init__(root, width=TABLE_WIDTH, height=TABLE_HEIGHT, bg=TABLE_COLOUR, bd=TABLE_BORDER)
        self.myBoard = None
        self.oppBoard = None
        self.gameText = tkinter.Text(self, height=20, width=35)
        self.gameText.grid(row=2, column=0, columnspan=1, rowspan=10, pady=(4, 0))
        self.gameText.insert("1.0", "None")

    def draw_board(self, gamestate, my_board):
        i = 0
        if my_board:
            output = "Your Current Guesses:\n"
            for guess in gamestate["MyAnswers"]:
                if guess:
                    output += str(i) + ". '" + str(guess) + "'\n"
                else:
                    output += str(i) + ". NO ANSWER \n"
                i += 1
            output += "\n\n\n"
            self.gameText.insert("1.0", output)
        else:
            output = "Opponent's Current Guesses:\n"
            for guess in gamestate["OppAnswers"]:
                if guess:
                    output += str(i) + ". '" + str(guess) + "'\n"
                else:
                    output += str(i) + ". NO ANSWER \n"
                i += 1
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
