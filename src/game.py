from typing import TYPE_CHECKING
import random
import pickle
from solver import SolveState
from game_board import ScrabbleBoard
from player_model import Player
from constants import LETTERS_BAG

if TYPE_CHECKING:
    from dawg_graph import DAWG


class Game:
    def __init__(self, board: "ScrabbleBoard" = None):
        self.board = board if board else ScrabbleBoard()
        self.letters_bag = LETTERS_BAG.copy()
        self.dictionary = self._get_dictionary()
        self.player_1 = Player()
        self.player_2 = Player()


    @staticmethod
    def _get_dictionary() -> "DAWG":
        print("opening pickle started")
        with open("data/scrabble_words_small.pickle", "rb") as openfile:
            dictionary = pickle.load(openfile)
        print("opening pickle finished")
        return dictionary

    def start_game(self):
        self.player_1.refill_rack(self.letters_bag)
        self.player_2.refill_rack(self.letters_bag)
        move_made = False
        while not move_made:
            move_made = self.player_1.make_move(
                self.dictionary,
                self.board,
                self.letters_bag,
                True
            )
            if move_made:
                return self.player_1
            move_made = self.player_2.make_move(
                self.dictionary,
                self.board,
                self.letters_bag,
                True
            )
            if move_made:
                return self.player_2

    def play_game(self):
        first_player: "Player" = self.start_game()
        second_player: "Player" = self.player_2 if first_player == self.player_1 else self.player_1
        while self.letters_bag:
            if second_player.rack:
                second_player.make_move(
                    self.dictionary,
                    self.board,
                    self.letters_bag,
                )
            if first_player.rack:
                first_player.make_move(
                    self.dictionary,
                    self.board,
                    self.letters_bag,
                )

# Game().play_game()
#
# board = ScrabbleBoard()
#
# player_1 = Player()
#
# letters_bag = LETTERS_BAG.copy()
#
# player_1.refill_rack(letters_bag)
#
# assert len(player_1.rack) == 7
#
# assert len(letters_bag) < len(LETTERS_BAG)
# move_made = False
# while not move_made:
#     move_made = player_1.make_move(trie, board, letters_bag, True)
#     if not move_made:
#         player_1.exchange_rack(letters_bag)
#
# print(board)
# move_made = False
# while not move_made:
#     move_made = player_1.make_move(trie, board, letters_bag)
#     if not move_made:
#         player_1.exchange_rack(letters_bag)
#
# print(board)












