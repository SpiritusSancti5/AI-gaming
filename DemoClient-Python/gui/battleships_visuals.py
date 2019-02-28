import os
import tkinter
import copy
from PIL import Image, ImageTk

ASSETS_PATH = 'assets/51'

TABLE_WIDTH = 360
TABLE_HEIGHT = 360
TABLE_COLOUR = '#DDDDDD'
TABLE_BORDER = 1

TABLE_ROWS = 9
TABLE_COLUMNS = 9
TABLE_CELLS = TABLE_ROWS * TABLE_COLUMNS

TILE_HEIGHT = int(TABLE_HEIGHT / TABLE_ROWS)
TILE_WIDTH = int(TABLE_WIDTH / TABLE_COLUMNS)


class BattleshipsVisuals(tkinter.Canvas):
    def __init__(self, root):
        super().__init__(root, width=TABLE_WIDTH, height=TABLE_HEIGHT, bg=TABLE_COLOUR, bd=TABLE_BORDER)
        self.photos = [None] * TABLE_CELLS
        self.images = [None] * TABLE_CELLS
        self.image_id = [None] * TABLE_CELLS
        self.myBoard = None
        self.oppBoard = None

    def add_asset(self, asset_name, row, column):
        path = os.path.join(ASSETS_PATH, asset_name)
        image = Image.open(path)
        image = image.resize((TILE_HEIGHT, TILE_WIDTH), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image.convert("RGB"))
        index = (row * TABLE_ROWS) + column

        self.image_id[index] = self.create_image(column*TILE_HEIGHT, row*TILE_WIDTH, image=photo, anchor='nw')
        self.photos[index] = photo
        self.images[index] = image

    def draw_board(self, board, my_board):
        for row in range(len(board)):
            for column in range(len(board[0])):
                if (my_board and (self.myBoard is None or board[row][column] != self.myBoard[row][column])) or (not my_board and (self.oppBoard is None or board[row][column] != self.oppBoard[row][column])):
                    if board[row][column] == "":
                        self.add_asset('sea.png', row, column)
                    elif board[row][column] == "M":
                        self.add_asset('miss.png', row, column)
                    elif board[row][column] == "L":
                        self.add_asset(get_land_image(board, row, column) + '.png', row, column)
                    elif board[row][column] == "LM":
                        self.add_asset(get_land_image(board, row, column) + '_miss.png', row, column)
                    elif board[row][column] == "H":
                        self.add_asset('hit.png', row, column)
                    elif "H" in board[row][column]:
                        self.add_asset(get_ship_image(board, row, column) + '_hit.png', row, column)
                    elif "S" in board[row][column]:
                        self.add_asset(get_ship_image(board, row, column) + '_hit.png', row, column)
                    else:
                        self.add_asset(get_ship_image(board, row, column) + '.png', row, column)
        if my_board:
            self.myBoard = copy.deepcopy(board)
        else:
            self.oppBoard = copy.deepcopy(board)

    def clear_board(self):
        self.delete("all")

    def draw_game_state(self, game_state, my_board):
        if my_board:
            self.draw_board(game_state["MyBoard"], my_board)
        else:
            self.draw_board(game_state["OppBoard"], my_board)


def get_land_image(board, i, j):
    above = False
    below = False
    left = False
    right = False
    # Check 4 adjacent tiles for land
    if i <= 0 or "L" in board[i - 1][j]:  # Above
        above = True
    if i >= len(board) - 1 or "L" in board[i + 1][j]:  # Below
        below = True
    if j <= 0 or "L" in board[i][j - 1]:  # Left
        left = True
    if j >= len(board[0]) - 1 or "L" in board[i][j + 1]:  # Right
        right = True

    if not above and below and not left and right:  # land_corner_se
        image = "land_corner_se"
    elif not above and below and left and not right:  # land_corner_sw
        image = "land_corner_sw"
    elif not above and below and left and right:  # land_s
        image = "land_s"
    elif above and not below and not left and right:  # land_corner_ne
        image = "land_corner_ne"
    elif above and below and not left and right:  # land_e
        image = "land_e"
    elif above and not below and left and not right:  # land_corner_nw
        image = "land_corner_nw"
    elif above and below and left and not right:  # land_w
        image = "land_w"
    elif above and not below and left and right:  # land_n
        image = "land_n"
    elif above and below and left and right:  # land_cove_
        # Check 4 adjacent corner tiles for land
        if not (i <= 0 or j <= 0 or "L" in board[i - 1][j - 1]):  # land_cove_se
            image = "land_cove_se"
        elif not (i >= len(board) - 1 or j <= 0 or "L" in board[i + 1][j - 1]):  # land_cove_sw
            image = "land_cove_ne"
        elif not (j >= len(board[0]) - 1 or i <= 0 or "L" in board[i - 1][j + 1]):  # land_cove_sw
            image = "land_cove_sw"
        elif not (j >= len(board[0]) - 1 or i >= len(board[i]) - 1 or "L" in board[i + 1][j + 1]):  # land_cove_nw
            image = "land_cove_nw"
        else:  # land
            image = "land"
    else:  # Not used, would be the case for a width 1 strip of land
        image = "err"
    return image


def get_ship_image(board, i, j):
    ship_num = "".join([i for i in board[i][j] if i.isdigit()])
    above = False
    below = False
    left = False
    right = False

    # Check 4 adjacent tiles for same ship
    if i > 0 and ship_num in board[i - 1][j]:  # Above
        above = True
    if i < len(board) - 1 and ship_num in board[i + 1][j]:  # Below
        below = True
    if j > 0 and ship_num in board[i][j - 1]:  # Left
        left = True
    if j < len(board[0]) - 1 and ship_num in board[i][j + 1]:  # Right
        right = True

    if above and not below:  # Ship end bottom
        image = "ship_end_s"
    elif below and not above:  # Ship end top
        image = "ship_end_n"
    elif above and below:  # Ship middle vertical
        image = "ship_middle_v"
    elif left and not right:  # Ship end right
        image = "ship_end_e"
    elif right and not left:  # Ship end left
        image = "ship_end_w"
    elif left and right:  # Ship middle horizontal
        image = "ship_middle_h"
    else:  # Not used, would be the case for a length 1 ship
        image = "err"
    return image
