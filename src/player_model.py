from typing import TYPE_CHECKING
import random
from solver import SolveState

if TYPE_CHECKING:
    from typing import List, Optional, Tuple
    from dawg_graph import DAWG
    from game_board import ScrabbleBoard


class Player:
    def __init__(self, strategy: int = 1):
        self.rack: "Optional[List[str]]" = []
        self.score: "int" = 0
        self.moves: "List[Tuple[str, int]]" = []
        self.strategy = strategy

    def refill_rack(self, letters_bag: "List[str]") -> None:
        for i in range(7 - len(self.rack)):
            if letters_bag:
                letter = letters_bag.pop(random.randrange(len(letters_bag)))
                self.rack.append(letter)

    def remove_from_rack_used_letters(self, used_letters_from_rack: "Optional[List[str]]"):
        for letter in used_letters_from_rack:
            if letter in self.rack:
                self.rack.remove(letter)

    def exchange_rack(self, letters_bag: "List[str]"):
        for i in range(len(self.rack)):
            letters_bag.append(self.rack.pop())
        self.refill_rack(letters_bag)

    def update_word_score(self, move: dict) -> None:
        self.score += move["score"]
        self.moves.append((move["word"], move["score"]))

    def make_move(
            self,
            dictionary: "DAWG",
            board: "ScrabbleBoard",
            letters_bag: "List[str]",
            is_first_move: bool = False
    ) -> dict | bool:
        solver = SolveState(
            dictionary=dictionary,
            board=board,
            rack=self.rack
        )
        if is_first_move:
            solver.get_options_for_first_move()
        else:
            solver.find_all_options()

        if not solver.legal_moves:
            self.exchange_rack(letters_bag)
            return False
        move = solver.get_best_move(self.strategy, letters_bag, board)
        used_letters_from_rack = board.place_word(
            move["word"],
            move["start_pos"],
            move["direction"],
            dictionary,
        )
        self.update_word_score(move)
        self.remove_from_rack_used_letters(used_letters_from_rack)
        self.refill_rack(letters_bag)
        # print(board)
        return move

    @staticmethod
    def place_word_on_board(board: "ScrabbleBoard", move: dict, dictionary: "DAWG"):
        if not dictionary.has_word(move["word"]):
            raise

