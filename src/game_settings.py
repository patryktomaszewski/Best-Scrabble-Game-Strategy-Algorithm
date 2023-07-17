from ast import literal_eval
from enum import Enum
import pandas as pd
from constants import LETTERS_BAG_MAPPING


class ColumnNames(str, Enum):
    NUMBER_OF_GAMES = "number_of_games"
    NUMBER_OF_PLAYERS = "number_of_players"
    PLAYERS_STRATEGIES = "players_strategies"
    FIELDS_TO_CHANGE = "fields_to_change"
    FIELDS_VALUES = "fields_values"
    BAG_LETTERS_TO_MODIFY = "bag_letters_to_modify"
    NUMBER_OF_LETTERS_IN_BAG = "number_of_letters_in_bag"
    USE_GUI = "use_gui"
    SAVE_GAME_RESULTS = "save_game_results"


class GameSettings:
    def __init__(self):
        self.number_of_games = 1
        self.number_of_players = 4
        self.players_strategies = [1 for i in range(self.number_of_players)]
        self.letters_bag = None
        self.bonus_squares = {}
        self.use_gui = False
        self.save_game_results = False
        self.parse_config_file()
        self.set_letters_bag()
        self.set_bonus_squares()
        self.set_players_strategies()

    def set_players_strategies(self) -> None:
        if players_strategies := getattr(self, ColumnNames.PLAYERS_STRATEGIES):
            self.players_strategies = players_strategies

    def set_bonus_squares(self) -> None:
        bonus_squares = {
            (0, 0): "TW", (0, 7): "TW", (0, 14): "TW",
            (7, 0): "TW", (7, 7): "DW", (7, 14): "TW",
            (14, 0): "TW", (14, 7): "TW", (14, 14): "TW",
            (1, 1): "DW", (2, 2): "DL", (3, 3): "TL", (4, 4): "DL",
            (1, 13): "DW", (2, 12): "DL", (3, 11): "TL", (4, 10): "DL",
            (13, 1): "DW", (12, 2): "DL", (11, 3): "TL", (10, 4): "DL",
            (13, 13): "DW", (12, 12): "DL", (11, 11): "TL", (10, 10): "DL"
        }
        if getattr(self, ColumnNames.FIELDS_TO_CHANGE):
            for pos, modifier in zip(getattr(self, ColumnNames.FIELDS_TO_CHANGE),
                                            getattr(self, ColumnNames.FIELDS_VALUES)):
                if modifier == "blank":
                    bonus_squares.pop(pos, None)
                else:
                    bonus_squares[pos] = modifier
        self.bonus_squares = bonus_squares

    def set_letters_bag(self) -> None:
        letter_bag_mapping = LETTERS_BAG_MAPPING.copy()
        if getattr(self, ColumnNames.BAG_LETTERS_TO_MODIFY):
            for letter, letter_count in zip(getattr(self, ColumnNames.BAG_LETTERS_TO_MODIFY),
                                            getattr(self, ColumnNames.NUMBER_OF_LETTERS_IN_BAG)):
                letter_bag_mapping[letter] = letter_count

        self.letters_bag = [letter for letter, letter_count in letter_bag_mapping.items() for _ in range(letter_count)]

    def parse_config_file(self) -> None:
        df = pd.read_csv('src/config_file/game_config.csv',
                         converters={
                             ColumnNames.PLAYERS_STRATEGIES: literal_eval,
                             ColumnNames.FIELDS_TO_CHANGE: literal_eval,
                             ColumnNames.FIELDS_VALUES: literal_eval,
                             ColumnNames.BAG_LETTERS_TO_MODIFY: literal_eval,
                             ColumnNames.NUMBER_OF_LETTERS_IN_BAG: literal_eval,
                             ColumnNames.USE_GUI: literal_eval,
                             ColumnNames.SAVE_GAME_RESULTS: literal_eval,
                         }
                         )

        for col_name in ColumnNames:
            df_value = df[col_name].tolist()[0]

            setattr(self, col_name.value, df_value)

settings = GameSettings()
