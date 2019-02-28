import tkinter
from PIL import ImageTk
import platform

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

ASSETS_PATH = 'assets/54'

TABLE_WIDTH = 360
TABLE_HEIGHT = 360
TABLE_COLOUR = '#DDDDDD'
TABLE_BORDER = 1

my_best = None
opp_best = None


class TravellingSalesdroneVisuals(tkinter.Canvas):
    def __init__(self, root):
        super().__init__(root, width=TABLE_WIDTH, height=TABLE_HEIGHT, bg=TABLE_COLOUR, bd=TABLE_BORDER)
        if WINDOWS:
            image = ImageTk.PhotoImage(file="{0}/background.png".format(ASSETS_PATH))
        else:
            image = ImageTk.PhotoImage(file="./{0}/background.png".format(ASSETS_PATH))
        self.gameText = tkinter.Text(self, height=10, width=35)
        self.map = tkinter.Canvas(self, width=220, height=220)
        self.gameText.grid(row=8, column=0, columnspan=1, rowspan=1, pady=(4, 0))
        self.map.grid(row=2, column=0, rowspan=5, pady=(4, 0))
        self.map.create_image(110, 110, image=image, tags='background')
        self.map.image = image
        self.gameText.insert("1.0", "None")
        self.prevState = None

    def draw_board(self, gamestate, my_board):
        global my_best
        global opp_best

        if my_board and gamestate["MyBestDistance"] and (not my_best or gamestate["MyBestDistance"] < my_best):
            my_best = gamestate["MyBestDistance"]
            if not opp_best or my_best < opp_best:
                self.gameText.insert("1.0", "You submitted an overall best of:" + str(my_best) + "\n")
            else:
                self.gameText.insert("1.0", "You submitted a personal best of:" + str(my_best) + "\n")
        elif not my_board and gamestate["OppBestDistance"] and (not opp_best or gamestate["OppBestDistance"] < opp_best):
            opp_best = gamestate["OppBestDistance"]
            if not my_best or my_best > opp_best:
                self.gameText.insert("1.0", "Your opponent submitted an overall best of:" + str(opp_best) + "\n")
            else:
                self.gameText.insert("1.0", "Your opponent submitted a personal best of:" + str(opp_best) + "\n")

        self.map.delete("lines")
        solution = None
        if my_board and gamestate["MyBestSolution"]:
            coords = gamestate["CityCoords"]
            solution = gamestate["MyBestSolution"]
            if not gamestate["OppBestDistance"] or gamestate["MyBestDistance"] < gamestate["OppBestDistance"]:
                for i in range(len(solution)):
                    self.map.create_line(coords[solution[i]][0]*2+10, coords[solution[i]][1]*2+10, coords[solution[(i+1) % len(coords)]][0]*2+10, coords[solution[(i+1) % len(coords)]][1]*2+10, width=2, smooth=True, fill='#EAD700', tags='lines')
            else:
                for i in range(len(solution)):
                    self.map.create_line(coords[solution[i]][0]*2+10, coords[solution[i]][1]*2+10, coords[solution[(i+1) % len(coords)]][0]*2+10, coords[solution[(i+1) % len(coords)]][1]*2+10, width=2, smooth=True, fill='#D5423F', tags='lines')

        if not my_board and gamestate["OppBestSolution"]:
            coords = gamestate["CityCoords"]
            solution = gamestate["OppBestSolution"]
            if not gamestate["MyBestDistance"] or gamestate["OppBestDistance"] < gamestate["MyBestDistance"]:
                for i in range(len(solution)):
                    self.map.create_line(coords[solution[i]][0]*2+10, coords[solution[i]][1]*2+10, coords[solution[(i+1) % len(coords)]][0]*2+10, coords[solution[(i+1) % len(coords)]][1]*2+10, width=2, fill='#EAD700', tags='lines')
            else:
                for i in range(len(solution)):
                    self.map.create_line(coords[solution[i]][0]*2+10, coords[solution[i]][1]*2+10, coords[solution[(i+1) % len(coords)]][0]*2+10, coords[solution[(i+1) % len(coords)]][1]*2+10, width=2, fill='#D5423F', tags='lines')

        for city, index in zip(gamestate["CityCoords"], range(len(gamestate["CityCoords"]))):
            if solution and solution[0] == index:
                self.map.create_oval((city[0]*2)-2+10, (city[1]*2)-2+10, (city[0]*2)+2+10, (city[1]*2)+2+10, outline='white', fill="white", tags='cities')
            else:
                self.map.create_oval((city[0]*2)-2+10, (city[1]*2)-2+10, (city[0]*2)+2+10, (city[1]*2)+2+10, fill="black", tags='cities')

    def clear_board(self):
        global my_best
        global opp_best
        my_best = None
        opp_best = None
        self.gameText.delete("1.0", tkinter.END)
        self.gameText.insert("1.0", "None")
        self.map.delete("lines")
        self.map.delete("cities")

    def draw_game_state(self, game_state, my_board):
        if self.prevState and game_state == self.prevState:
            return
        if my_board:
            self.draw_board(game_state, my_board)
        else:
            self.draw_board(game_state, my_board)
        self.prevState = game_state
