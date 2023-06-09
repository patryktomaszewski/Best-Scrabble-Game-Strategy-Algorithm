from typing import TYPE_CHECKING
import random
import pickle
from solver import SolveState
from game_board import ScrabbleBoard
from player_model import Player
from game_settings import settings

if TYPE_CHECKING:
    from dawg_graph import DAWG
    from typing import List


class GameManager:
    def __init__(self, dictionary: "DAWG" = None):
        self.board = ScrabbleBoard()
        self.players_number = settings.number_of_players
        self.letters_bag = settings.letters_bag.copy()
        self.dictionary = dictionary if dictionary else self.get_dictionary()
        self.players: "List[Player]" = []
        self.course_of_the_game = []
        if settings.players_strategies and len(settings.players_strategies) != self.players_number:
            raise f"Players strategies number must be equal to players number." \
                  f" Given: players strategies: {settings.players_strategies}, players number: {self.players_number}"
        if settings.players_strategies:
            for strategy in settings.players_strategies:
                self.players.append(Player(strategy=strategy))
        else:
            for i in range(self.players_number):
                self.players.append(Player())

    @staticmethod
    def get_dictionary() -> "DAWG":
        print("opening pickle started")
        with open("data/scrabble_words_small.pickle", "rb") as openfile:
            dictionary = pickle.load(openfile)
        print("opening pickle finished")
        return dictionary

    def update_course_of_the_game_if_move_made(self, move_made: dict | bool, player_id: int) -> None:
        if move_made:
            self.course_of_the_game.append((player_id, move_made))

    def start_game(self):
        for player in self.players:
            player.refill_rack(self.letters_bag)
        # self.player_1.refill_rack(self.letters_bag)
        # self.player_2.refill_rack(self.letters_bag)
        move_made = False
        while not move_made:
            for idx, player in enumerate(self.players):
                move_made = player.make_move(
                    self.dictionary,
                    self.board,
                    self.letters_bag,
                    True
                )
                if move_made:
                    self.update_course_of_the_game_if_move_made(move_made, idx)
                    return idx, player

    def play_game(self):
        idx, first_player = self.start_game()
        first_move = True
        # finish game if each player hasn't played word since 4 rounds
        no_word_played_iterator = 0
        while self.letters_bag or (no_word_played_iterator <= 16):
            if first_move:
                for idx, player in enumerate(self.players[idx:], idx):
                    move_made = player.make_move(
                        self.dictionary,
                        self.board,
                        self.letters_bag,
                    )
                    self.update_course_of_the_game_if_move_made(move_made, idx)
                first_move = False
            else:
                for idx, player in enumerate(self.players):
                    move_made = player.make_move(
                        self.dictionary,
                        self.board,
                        self.letters_bag,
                    )
                    if not move_made:
                        no_word_played_iterator += 1
                    else:
                        no_word_played_iterator = 0
                    self.update_course_of_the_game_if_move_made(move_made, idx)

