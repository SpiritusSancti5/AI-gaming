import tkinter

ASSETS_PATH = 'assets/0'

TABLE_WIDTH = 360
TABLE_HEIGHT = 360
TABLE_COLOUR = '#DDDDDD'
TABLE_BORDER = 1


class NullVisuals(tkinter.Canvas):
    def __init__(self, root):
        super().__init__(root, width=TABLE_WIDTH, height=TABLE_HEIGHT, bg=TABLE_COLOUR, bd=TABLE_BORDER)
        self.chooseGameType = tkinter.Label(self, text="Please select a game type")
        self.chooseGameType.grid(row=1, column=1)

    def clear_board(self):
        pass

    def draw_game_state(self, game_state, my_board):
        pass
