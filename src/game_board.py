from typing import TYPE_CHECKING
from constants import LETTER_SCORES
from exceptions import WordDoesNotExistError

if TYPE_CHECKING:
    from typing import Tuple, List, Optional
    from dawg_graph import DAWG


class ScrabbleBoard:
    def __init__(self, size=15):
        # Initialize the board as a 2D list of None values
        self.size = size
        self.board = [[None] * size for i in range(size)]
        # Set up the bonus squares
        self.bonus_squares = {
            (0, 0): "TW", (0, 7): "TW", (0, 14): "TW",
            (7, 0): "TW", (7, 7): "DW", (7, 14): "TW",
            (14, 0): "TW", (14, 7): "TW", (14, 14): "TW",
            (1, 1): "DW", (2, 2): "DL", (3, 3): "TL", (4, 4): "DL",
            (1, 13): "DW", (2, 12): "DL", (3, 11): "TL", (4, 10): "DL",
            (13, 1): "DW", (12, 2): "DL", (11, 3): "TL", (10, 4): "DL",
            (13, 13): "DW", (12, 12): "DL", (11, 11): "TL", (10, 10): "DL"
        }
        self.letter_scores = LETTER_SCORES

    def is_valid_position(self, pos: "Tuple[int, int]"):
        # Check if a given position is within the board boundaries
        row, col = pos
        return row >= 0 and col >= 0 and row < self.size and col < self.size

    def is_filled(self, pos, empty_positions: "Optional[List[Tuple[int, int]]]" = None) -> bool:
        if not empty_positions:
            empty_positions = self.get_empty_positions()
        return self.is_valid_position(pos) and pos not in empty_positions


    def is_empty(self, pos, empty_positions: "Optional[List[Tuple[int, int]]]" = None) -> bool:
        if not empty_positions:
            empty_positions = self.get_empty_positions()
        return self.is_valid_position(pos) and pos in empty_positions

    def get_letter_score(self, letter):
        # Return the score of a given letter
        return self.letter_scores.get(letter, 0)

    def get_word_score(self, word, pos, direction: "str", wild_card_idxes: "List[int]"):
        # Compute the score of a given word placed on the board at a given position and orientation
        x, y = pos
        score = 0
        word_multiplier = 1
        for i, letter in enumerate(word):
            if direction == "across":
                pos_x, pos_y = x + i, y
            else:
                pos_x, pos_y = x, y + i
            if self.is_valid_position((pos_x, pos_y)):
                letter_multiplier = 1
                if (pos_x, pos_y) in self.bonus_squares:
                    bonus_square = self.bonus_squares[(pos_x, pos_y)]
                    if bonus_square == "DW":
                        letter_multiplier = 2
                    elif bonus_square == "TW":
                        word_multiplier *= 3
                    elif bonus_square == "DL":
                        letter_multiplier = 2
                    elif bonus_square == "TL":
                        letter_multiplier = 3
                if i in wild_card_idxes:
                    letter = "%"
                score += self.get_letter_score(letter) * letter_multiplier
            else:
                return 0
        return score * word_multiplier

    def place_word(self, word: str, pos: "Tuple[int, int]", direction: "str", dictionary: "DAWG") -> None:
        # Place a given word on the board at a given position and orientation
        if not dictionary.has_word(word):
            raise WordDoesNotExistError(word)
        x, y = pos
        if self.is_valid_position(pos):
            for i, letter in enumerate(word):
                if direction == "across":
                    pos_x, pos_y = x, y + i
                else:
                    pos_x, pos_y = x + i, y
                if self.is_valid_position((pos_x, pos_y)):
                    self.board[pos_x][pos_y] = letter
                    # print(f"{pos_x}, {pos_y}")

    def remove_word(self, word, pos, direction: "str"):
        # Remove a given word from the board at a given position and orientation
        x, y = pos
        if self.is_valid_position(pos):
            for i, letter in enumerate(word):
                if direction == "across":
                    pos_x, pos_y = x + i, y
                else:
                    pos_x, pos_y = x, y + i
                if self.is_valid_position((pos_x, pos_y)):
                    self.board[pos_x][pos_y] = None

    def get_board(self):
        # Return a copy of the current board
        return [row[:] for row in self.board]

    def get_empty_positions(self) -> "List[Tuple[int, int]]":
        empty_positions = []
        for row_idx, row in enumerate(self.board):
            [empty_positions.append((row_idx, col_idx)) for col_idx, letter in enumerate(row) if letter is None]
        return empty_positions

    def get_all_positions(self) -> "List[Tuple[int, int]]":
        empty_positions = []
        for row_idx, row in enumerate(self.board):
            [empty_positions.append((row_idx, col_idx)) for col_idx, letter in enumerate(row)]
        return empty_positions

    def get_cell(self, position: "Tuple[int, int]") -> "Optional[str]":
        row, col = position
        return self.board[row][col]

    def __str__(self):
        # Return a string representation of the board for printing
        result = ""
        for row in self.board:
            result += " ".join([str(letter) if letter is not None else "." for letter in row]) + "\n"
        return result
