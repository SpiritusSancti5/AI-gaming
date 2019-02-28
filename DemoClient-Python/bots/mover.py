persistentData = {}  # Needs to be at top of file

from bots import battleships_bot
from bots import noughts_and_crosses_bot
from bots import travelling_salesdrone_bot
from bots import predictive_text_bot
from bots import twist_cube_bot
from bots import sliding_puzzle_bot
from bots import blurry_word_bot
from bots import mastermind_bot
from bots import warehouse_logistics_bot
from bots import four_in_a_row_bot
from bots import who_is_who_bot
from bots import reversing_stones_bot
from bots import checkers_bot
from bots import go_bot
from bots import lexico_bot
from bots import dominoes_bot
from bots import match_game_bot

import json


def calculate_move(game_type, gamestate):
    config = json.load(open('config.json', 'r'))
    if game_type == config["BATTLESHIPS_GAME_TYPE_ID"]:
        return battleships_bot.calculateMove(gamestate)
    elif game_type == config["NOUGHTS_AND_CROSSES_GAME_TYPE_ID"]:
        return noughts_and_crosses_bot.calculateMove(gamestate)
    elif game_type == config["TRAVELLING_SALESDRONE_GAME_TYPE_ID"]:
        return travelling_salesdrone_bot.calculateMove(gamestate)
    elif game_type == config["PREDICTIVE_TEXT_GAME_TYPE_ID"]:
        return predictive_text_bot.calculateMove(gamestate)
    elif game_type == config["TWIST_CUBE_GAME_TYPE_ID"]:
        return twist_cube_bot.calculateMove(gamestate)
    elif game_type == config["SLIDING_PUZZLE_GAME_TYPE_ID"]:
        return sliding_puzzle_bot.calculateMove(gamestate)
    elif game_type == config["BLURRY_WORD_GAME_TYPE_ID"]:
        return blurry_word_bot.calculateMove(gamestate)
    elif game_type == config["MASTERMIND_GAME_TYPE_ID"]:
        return mastermind_bot.calculateMove(gamestate)
    elif game_type == config["WAREHOUSE_LOGISTICS_GAME_TYPE_ID"]:
        return warehouse_logistics_bot.calculateMove(gamestate)
    elif game_type == config["FOUR_IN_A_ROW_GAME_TYPE_ID"]:
        return four_in_a_row_bot.calculateMove(gamestate)
    elif game_type == config["WHO_IS_WHO_GAME_TYPE_ID"]:
        return who_is_who_bot.calculateMove(gamestate)
    elif game_type == config["REVERSING_STONES_GAME_TYPE_ID"]:
        return reversing_stones_bot.calculateMove(gamestate)
    elif game_type == config["CHECKERS_GAME_TYPE_ID"]:
        return checkers_bot.calculateMove(gamestate)
    elif game_type == config["GO_GAME_TYPE_ID"]:
        return go_bot.calculateMove(gamestate)
    elif game_type == config["LEXICO_GAME_TYPE_ID"]:
        return lexico_bot.calculateMove(gamestate)
    elif game_type == config["DOMINOES_GAME_TYPE_ID"]:
        return dominoes_bot.calculateMove(gamestate)
    elif game_type == config["MATCH_GAME_TYPE_ID"]:
        return match_game_bot.calculateMove(gamestate)
