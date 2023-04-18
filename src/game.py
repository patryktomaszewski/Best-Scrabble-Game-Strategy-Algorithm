from typing import TYPE_CHECKING
import random
import pickle
from solver import SolveState
from game_board import ScrabbleBoard
from player_model import Player
from constants import LETTERS_BAG

if TYPE_CHECKING:
    from dawg_graph import DAWG
    from typing import List


class Game:
    def __init__(self, board: "ScrabbleBoard" = None, players_number: int = 2, dictionary: "DAWG" = None,
                 players_strategies: "List[int]" = None):
        self.board = board if board else ScrabbleBoard()
        self.letters_bag = LETTERS_BAG.copy()
        self.dictionary = dictionary if dictionary else self.get_dictionary()
        self.players = []
        if players_strategies and len(players_strategies) != players_number:
            raise f"Players strategies number must be equal to players number." \
                  f" Given: players strategies: {players_strategies}, players number: {players_number}"
        if players_strategies:
            for strategy in players_strategies:
                self.players.append(Player(strategy=strategy))
        else:
            for i in range(players_number):
                self.players.append(Player())

    @staticmethod
    def get_dictionary() -> "DAWG":
        print("opening pickle started")
        with open("data/scrabble_words_complete.pickle", "rb") as openfile:
            dictionary = pickle.load(openfile)
        print("opening pickle finished")
        return dictionary

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
                    return idx, player

    def play_game(self):
        idx, first_player = self.start_game()
        first_move = True
        while self.letters_bag:
            if first_move:
                for player in self.players[idx:]:
                    player.make_move(
                    self.dictionary,
                    self.board,
                    self.letters_bag,
                )
            else:
                for player in self.players:
                    player.make_move(
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












