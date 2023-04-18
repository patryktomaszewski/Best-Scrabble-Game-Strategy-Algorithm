from typing import TYPE_CHECKING
from constants import AVAILABLE_LETTERS, RARE_LETTER

if TYPE_CHECKING:
    from game_board import ScrabbleBoard
    from typing import List, Tuple, Optional, Dict
    from dawg_graph import DAWG


class SolveState:
    def __init__(self, dictionary: "DAWG", board: "ScrabbleBoard", rack):
        self.dictionary: "DAWG" = dictionary
        self.game_board: ScrabbleBoard = board
        self.rack: "List[str]" = rack
        self.cross_check_results = None
        self.direction: "Optional[str]" = None
        self.legal_moves: "Optional[List[dict]]" = []
        self.wild_card_idxes = []

    def before(self, pos):
        row, col = pos
        if self.direction == 'across':
            return row, col - 1
        else:
            return row - 1, col

    def after(self, pos):
        row, col = pos
        if self.direction == 'across':
            return row, col + 1
        else:
            return row + 1, col

    def before_cross(self, pos):
        row, col = pos
        if self.direction == 'across':
            return row - 1, col
        else:
            return row, col - 1

    def after_cross(self, pos):
        row, col = pos
        if self.direction == 'across':
            return row + 1, col
        else:
            return row, col + 1

    def legal_move(self, word, last_pos):
        play_pos = last_pos
        start_pos = play_pos
        word_idx = len(word) - 1
        while word_idx >= 0:
            start_pos = play_pos
            word_idx -= 1
            play_pos = self.before(play_pos)

        self.legal_moves.append({
            "score": self.game_board.get_word_score(word, start_pos, self.direction, self.wild_card_idxes),
            "word": word,
            "direction": self.direction,
            "start_pos": start_pos,
        })

    @staticmethod
    def get_most_pointed_move(legal_moves) -> dict:
        """
        returns move which is most pointed
        """
        best_move = max(legal_moves, key=lambda x: x['score'])
        return best_move

    @staticmethod
    def get_longest_word(legal_moves) -> dict:
        best_move = max(legal_moves, key=lambda x: len(x['word']))
        return best_move

    @staticmethod
    def get_shortest_word(legal_moves) -> dict:
        best_move = min(legal_moves, key=lambda x: len(x['word']))
        return best_move

    @staticmethod
    def get_move_with_most_rare_letters(legal_moves) -> dict:
        best_move = max(legal_moves, key=lambda x: sum(map(x['word'].count, RARE_LETTER)) )
        return best_move

    def get_best_move(self, strategy: int) -> dict:
        """
        get best move based on word score
        """
        if strategy == 1:
            best_move = self.get_most_pointed_move(self.legal_moves)
        elif strategy == 2:
            best_move = self.get_longest_word(self.legal_moves)
        elif strategy == 3:
            best_move = self.get_shortest_word(self.legal_moves)
        elif strategy == 4:
            best_move = self.get_move_with_most_rare_letters(self.legal_moves)

        return best_move

    def cross_check(self) -> "Dict[Tuple[int, int], List[str]]":
        result = dict()
        empty_positions = self.game_board.get_empty_positions()
        for pos in empty_positions:
            letters_before = ""
            scan_pos = pos
            while self.game_board.is_filled(self.before_cross(scan_pos), empty_positions):
                scan_pos = self.before_cross(scan_pos)
                letters_before = self.game_board.get_cell(scan_pos) + letters_before
            letters_after = ""
            scan_pos = pos
            while self.game_board.is_filled(self.after_cross(scan_pos), empty_positions):
                scan_pos = self.after_cross(scan_pos)
                letters_after = letters_after + self.game_board.get_cell(scan_pos)
            if len(letters_before) == 0 and len(letters_after) == 0:
                legal_here = AVAILABLE_LETTERS
            else:
                legal_here = []
                for letter in AVAILABLE_LETTERS:
                    word_formed = letters_before + letter + letters_after
                    if self.dictionary.has_word(word_formed):
                        legal_here.append(letter)
            result[pos] = legal_here
        return result

    def find_anchors(self) -> "List[Tuple[int, int]]":
        """
        finds cells where we potentially can start word
        - is empty
        - has neighbour
        """
        anchors = []
        empty_positions = self.game_board.get_empty_positions()
        for empty_pos in empty_positions:
            if (
                    self.game_board.is_filled(self.before(empty_pos), empty_positions) or
                    self.game_board.is_filled(self.after(empty_pos), empty_positions) or
                    self.game_board.is_filled(self.before_cross(empty_pos), empty_positions) or
                    self.game_board.is_filled(self.after_cross(empty_pos), empty_positions)
            ):
                anchors.append(empty_pos)
        return anchors

    def before_part(self, partial_word, current_node, anchor_pos, limit):
        self.extend_after(partial_word, current_node, anchor_pos, False)
        if limit > 0:
            for next_letter in current_node.edges.keys():
                if next_letter in self.rack:
                    self.rack.remove(next_letter)
                    self.before_part(
                        partial_word + next_letter,
                        current_node.edges[next_letter],
                        anchor_pos,
                        limit - 1
                    )
                    self.rack.append(next_letter)
                elif "%" in self.rack:
                    self.rack.remove("%")
                    expanded__word = partial_word + next_letter
                    self.wild_card_idxes.append(len(expanded__word) - 1)
                    self.before_part(
                        expanded__word,
                        current_node.edges[next_letter],
                        anchor_pos,
                        limit - 1
                    )
                    self.rack.append("%")

    def extend_after(self, partial_word, current_node, next_pos, anchor_filled):
        empty_positions = self.game_board.get_empty_positions()
        if self.game_board.is_empty(next_pos, empty_positions) and current_node.final and anchor_filled:
            self.legal_move(partial_word, self.before(next_pos))
        if self.game_board.is_valid_position(next_pos):
            if self.game_board.is_empty(next_pos):
                for next_letter in current_node.edges.keys():
                    if next_letter in self.cross_check_results[next_pos]:
                        if next_letter in self.rack:
                            self.rack.remove(next_letter)
                            self.extend_after(
                                partial_word + next_letter,
                                current_node.edges[next_letter],
                                self.after(next_pos),
                                True
                            )
                            self.rack.append(next_letter)
                        elif "%" in self.rack:
                            self.rack.remove("%")
                            expanded_word = partial_word + next_letter
                            self.wild_card_idxes.append(len(expanded_word) - 1)
                            self.extend_after(
                                expanded_word,
                                current_node.edges[next_letter],
                                self.after(next_pos),
                                True
                            )
                            self.rack.append("%")

            else:
                existing_letter = self.game_board.get_cell(next_pos)
                if existing_letter in current_node.edges.keys():
                    self.extend_after(
                        partial_word + existing_letter,
                        current_node.edges[existing_letter],
                        self.after(next_pos),
                        True
                    )

    def find_all_options(self):
        for direction in ['across', 'down']:
            self.direction = direction
            anchors = self.find_anchors()
            # print(anchors)
            self.cross_check_results = self.cross_check()
            empty_positions = self.game_board.get_empty_positions()
            for anchor_pos in anchors:
                self.wild_card_idxes = []
                if self.game_board.is_filled(self.before(anchor_pos), empty_positions):
                    scan_pos = self.before(anchor_pos)
                    partial_word = self.game_board.get_cell(scan_pos)
                    while self.game_board.is_filled(self.before(scan_pos), empty_positions):
                        scan_pos = self.before(scan_pos)
                        partial_word = self.game_board.get_cell(scan_pos) + partial_word

                    pw_node = self.dictionary.lookup(partial_word)
                    if pw_node is not None:
                        self.extend_after(
                            partial_word,
                            pw_node,
                            anchor_pos,
                            False
                        )
                else:
                    limit = 0
                    scan_pos = anchor_pos
                    while self.game_board.is_empty(self.before(scan_pos), empty_positions) and self.before(scan_pos) not in anchors:
                        limit = limit + 1
                        scan_pos = self.before(scan_pos)
                    self.before_part("", self.dictionary.root, anchor_pos, limit)

    def get_options_for_first_move(self):
        anchor_pos = (7, 8)
        empty_positions = self.game_board.get_empty_positions()
        for direction in ['across', 'down']:
            self.direction = direction
            self.cross_check_results = self.cross_check()
            limit = 0
            scan_pos = anchor_pos
            while self.game_board.is_empty(self.before(scan_pos), empty_positions):
                limit = limit + 1
                scan_pos = self.before(scan_pos)
            self.before_part("", self.dictionary.root, anchor_pos, limit)
        a = 2
        #     self.direction = direction
        #     self.cross_check_results = self.cross_check()
        #     self.before_part("", self.dictionary.root, (7,7), 8)
        # for letter in self.rack:
        #     self.game_board.board[7][8] = letter
        #     self.rack.remove(letter)
        #     self.find_all_options()
        #     self.rack.append(letter)
        #     self.game_board.board[7][8] = None
