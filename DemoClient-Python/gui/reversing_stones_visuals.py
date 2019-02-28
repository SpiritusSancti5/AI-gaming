import tkinter

ASSETS_PATH = 'assets/67'

TABLE_WIDTH = 360
TABLE_HEIGHT = 360
TABLE_COLOUR = '#DDDDDD'
TABLE_BORDER = 1


class ReversingStonesVisuals(tkinter.Canvas):
    def __init__(self, root):
        super().__init__(root, width=TABLE_WIDTH, height=TABLE_HEIGHT, bg=TABLE_COLOUR, bd=TABLE_BORDER)
        self.myBoard = None
        self.oppBoard = None
        self.gameText = tkinter.Text(self, height=20, width=35)
        self.gameText.grid(row=2, column=0, columnspan=1, rowspan=10, pady=(4, 0))
        self.gameText.insert("1.0", "None")

    def draw_board(self, gamestate, my_board):
        if my_board:
            output = "Your Role: {0}\n".format(gamestate["Role"])
            output += self.make_board(gamestate["Board"])
            output += "\n\n\n"
            self.gameText.insert("1.0", output)

    def make_board(self, board):
        output = ""
        for row in board:
            output += "|"
            for cell in row:
                output += " " if cell == -1 else str(cell)
            output += "|\n"
        return output

    def clear_board(self):
        self.gameText.delete("1.0", tkinter.END)
        self.gameText.insert("1.0", "None")

    def draw_game_state(self, game_state, my_board):
        if my_board:
            self.draw_board(game_state, my_board)
        else:
            self.draw_board(game_state, my_board)
