from typing import TYPE_CHECKING
from constants import LETTER_SCORES
from exceptions import WordDoesNotExistError
from game_settings import settings

if TYPE_CHECKING:
    from typing import Tuple, List, Optional
    from dawg_graph import DAWG


class ScrabbleBoard:
    def __init__(self, size=15):
        # Initialize the board as a 2D list of None values
        self.size = size
        self.board = [[None] * size for i in range(size)]
        # Set up the bonus squares
        self.bonus_squares = settings.bonus_squares
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

    def get_word_score(self, word, pos, direction: "str", rack: "List[str]"):
        # Compute the score of a given word placed on the board at a given position and orientation
        empty_positions = self.get_empty_positions()
        used_letters_count = 0
        used_letters = []
        used_letters_with_blanks = []
        wild_card_idxes = []
        x, y = pos
        score = 0
        word_multiplier = 1
        fifty_points_bonus = 0
        was_fifty_points_bonus = False
        for i, letter in enumerate(word):
            if direction == "across":
                pos_x, pos_y = x, y + i
            else:
                pos_x, pos_y = x + i, y
            if self.is_filled((pos_x, pos_y), empty_positions):
                continue
            if self.is_valid_position((pos_x, pos_y)):
                used_letters_count += 1
                letter_multiplier = 1
                used_letters.append(letter)
                used_letters_with_blanks.append(letter)
                if (pos_x, pos_y) in self.bonus_squares:
                    bonus_square = self.bonus_squares[(pos_x, pos_y)]
                    if bonus_square == "DW":
                        word_multiplier *= 2
                    elif bonus_square == "TW":
                        word_multiplier *= 3
                    elif bonus_square == "DL":
                        letter_multiplier = 2
                    elif bonus_square == "TL":
                        letter_multiplier = 3
                if letter not in rack:
                    used_letters.remove(letter)
                    wild_card_idxes.append(i)
                    letter = "%"

                fifty_points_bonus = 0
                was_fifty_points_bonus = False
                if used_letters_count == 7:
                    fifty_points_bonus = 50
                    was_fifty_points_bonus = True
                score += self.get_letter_score(letter) * letter_multiplier
            else:
                return None, None, None, None, None
        return score * word_multiplier + fifty_points_bonus, was_fifty_points_bonus, wild_card_idxes, used_letters, used_letters_with_blanks

    def place_word(self, word: str, pos: "Tuple[int, int]", direction: "str",
                    dictionary: "DAWG") -> "Optional[List[str]]":
        # Place a given word on the board at a given position and orientation
        if not dictionary.has_word(word):
            raise WordDoesNotExistError(word)
        x, y = pos
        used_letters_from_rack = []
        if self.is_valid_position(pos):
            for i, letter in enumerate(word):
                if direction == "across":
                    pos_x, pos_y = x, y + i
                else:
                    pos_x, pos_y = x + i, y
                if self.is_valid_position((pos_x, pos_y)):
                    if not self.board[pos_x][pos_y]:
                        used_letters_from_rack.append(letter)
                    self.board[pos_x][pos_y] = letter
        return used_letters_from_rack

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
