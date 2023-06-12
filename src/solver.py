from typing import TYPE_CHECKING
from constants import AVAILABLE_LETTERS, RARE_LETTER, VOWELS

if TYPE_CHECKING:
    from game_board import ScrabbleBoard
    from typing import List, Tuple, Optional, Dict
    from dawg_graph import DAWG


class SolveState:
    def __init__(self, dictionary: "DAWG", board: "ScrabbleBoard", rack):
        self.dictionary: "DAWG" = dictionary
        self.game_board: ScrabbleBoard = board
        self.rack: "List[str]" = rack
        self._not_changeable_rack: "List[str]" = rack.copy()
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

        score, was_fifty_points_bonus, wild_card_idxes, used_letters, used_letters_with_blanks = self.game_board.get_word_score(
            word, start_pos, self.direction, self._not_changeable_rack)

        if score is None or was_fifty_points_bonus is None or wild_card_idxes is None:
            return
        self.legal_moves.append({
            "score": score,
            "word": word,
            "direction": self.direction,
            "start_pos": start_pos,
            "wild_card_idxes": wild_card_idxes,
            "fifty_score_bonus": was_fifty_points_bonus,
            "used_letters": used_letters,
            "used_letters_with_blanks": used_letters_with_blanks,
            "used_letters_no_repetition": set(used_letters),
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
        best_move = max(legal_moves, key=lambda x: sum(map(x['word'].count, RARE_LETTER)))
        return best_move

    @staticmethod
    def get_move_with_least_rare_letters(legal_moves) -> dict:
        best_move = min(legal_moves, key=lambda x: sum(map(x['word'].count, RARE_LETTER)))
        return best_move

    def get_rid_off_most_letters_at_the_end(self, legal_moves, letters_bag: "List[str]") -> dict:
        if len(letters_bag) < 10:
            return self.get_longest_word(legal_moves)
        else:
            return self.get_most_pointed_move(legal_moves)


    @staticmethod
    def set_used_letters_from_rack(legal_moves, board: "ScrabbleBoard") -> None:
        used_letters_from_rack = 0
        for legal_move in legal_moves:
            pos_x, pos_y = legal_move["start_pos"]
            for i, letter in enumerate(legal_move["word"]):
                if not board.board[pos_x][pos_y]:
                    used_letters_from_rack += 1
                if legal_move["direction"] == "across":
                    pos_x, pos_y = pos_x, pos_y + i
                else:
                    pos_x, pos_y = pos_x + i, pos_y
            legal_move["used_letters_from_rack"] = used_letters_from_rack

    @staticmethod
    def set_bonus_field_count(legal_moves, board: "ScrabbleBoard") -> None:
        bonus_fields_count = 0
        for legal_move in legal_moves:
            pos_x, pos_y = legal_move["start_pos"]
            for i, letter in enumerate(legal_move["word"]):
                if not board.bonus_squares.get((pos_x, pos_y)):
                    bonus_fields_count += 1
                if legal_move["direction"] == "across":
                    pos_x, pos_y = pos_x, pos_y + i
                else:
                    pos_x, pos_y = pos_x + i, pos_y
            legal_move["bonus_fields_count"] = bonus_fields_count



    @staticmethod
    def get_move_with_the_most_letters_from_rack(legal_moves) -> dict:
        best_move = max(legal_moves, key=lambda x: x['used_letters_from_rack'])
        return best_move

    @staticmethod
    def get_move_with_least_letters_from_rack(legal_moves) -> dict:
        best_move = min(legal_moves, key=lambda x: x['used_letters_from_rack'])
        return best_move

    @staticmethod
    def get_move_with_most_bonus_fields(legal_moves) -> dict:
        best_move = max(legal_moves, key=lambda x: x['bonus_fields_count'])
        return best_move

    @staticmethod
    def get_move_with_wild_card_strategy(legal_moves) -> dict:
        """
        play wild card when store with using it is 25 pt better than second
        highest without using them
        """
        best_move = max(legal_moves, key=lambda x: x['score'])
        legal_moves_without_wild_card = list(filter(lambda a: len(a["wild_card_idxes"]) == 0, legal_moves))
        if legal_moves_without_wild_card:
            without_card = max(legal_moves_without_wild_card, key = lambda x: x['score'])
            if (best_move["score"] - without_card["score"]) < 25:
                best_move = without_card

        return best_move

    def _strategy_with_blanks_for_one_move(self, legal_moves: "List[dict]", move_with_best_score: dict, letters_bag: "List[str]", best_score_move: dict):
        """
        - if it is not a word arranged with all the letters from the tray, and two blanks or one blanks were used,
         but at the same time the other one was not already used on the board,
          then do not take this word, take the less scored one, which leaves alone the blanks you have,
        - or, take the one with the blank(s) if the next on the list of highest scoring is more than 25 points weaker,
        """
        fifty_score_bonus = move_with_best_score["fifty_score_bonus"]
        number_of_used_blanks = len(move_with_best_score["wild_card_idxes"])
        without_best_score = list(filter(lambda a: a["score"] != best_score_move["score"], legal_moves))
        sorted_by_score = sorted(without_best_score, key=lambda d: d['score'], reverse=True)
        second_score_move = sorted_by_score[0]

        if (not fifty_score_bonus) and (number_of_used_blanks == 2 or (number_of_used_blanks == 1 and letters_bag.count("%") == 1)):
            if second_score_move["score"] > 25:
                best_move = second_score_move
            else:
                best_move = best_score_move
        else:
            best_move = best_score_move
        return best_move

    @staticmethod
    def are_all_letters_vowels(letters: "List[str]") -> bool:
        vowels_in_letters = list(filter(lambda a: a in VOWELS, letters))
        if len(vowels_in_letters) == letters:
            return True
        return False

    @staticmethod
    def are_all_letters_consonants(letters: "List[str]") -> bool:
        consonants_in_letters = list(filter(lambda a: a not in  VOWELS, letters))
        if len(consonants_in_letters) == letters:
            return True
        return False


    def get_move_with_no_imbalance(self, legal_moves: "List[dict]"):
        """
        if there are only vowels or only consonants left on the rack find a less
         punctuated word that doesn't do that
        """
        sorted_moves = sorted(legal_moves, key=lambda d: d['score'], reverse=True)
        best_move = legal_moves[-1]

        for move in sorted_moves:
            left_words_in_rack = self._not_changeable_rack.copy()
            [left_words_in_rack.remove(letter) for letter in move["used_letters"]]
            # we do not take blanks in calculations
            left_words_in_rack = [x for x in left_words_in_rack if x != '%']

            if len(left_words_in_rack) > 2:
                if self.are_all_letters_vowels(left_words_in_rack):
                    continue
                if self.are_all_letters_consonants(left_words_in_rack):
                    continue
            best_move = move
        return best_move

    @staticmethod
    def get_word_with_highest_points_to_used_letters_ratio(legal_moves) -> dict:
        """

        Calculate the ratio "number of points / number of letters used"
        and choose the word with the highest / lowest ratio (the letters
        used from the board - only from the rack - the idea is to increase
        the chances of extending words),
        """
        best_move = max(legal_moves, key=lambda x: x["score"]/len(x['word']))
        return best_move

    @staticmethod
    def get_word_with_lowest_points_to_used_letters_ratio(legal_moves) -> dict:
        """

        Calculate the ratio "number of points / number of letters used"
        and choose the word with the highest / lowest ratio (the letters
        used from the board - only from the rack - the idea is to increase
        the chances of extending words),
        """
        best_move = min(legal_moves, key=lambda x: x["score"] / len(x['word']))
        return best_move

    @staticmethod
    def get_word_using_most_double_letters(legal_moves: "List[dict]") -> dict:
        """
        Choose a word that gets rid of duplicate letters
        """
        best_move = max(legal_moves, key=lambda x: x["used_letters_no_repetition"])
        return best_move


    def complex_strategy_1(self, legal_moves: "List[dict]", letters_bag: "List[str]", strategy: int) -> dict:
        best_score_move = max(legal_moves, key=lambda x: x['score'])
        moves_with_best_score = list(filter(lambda a: a["score"] == best_score_move["score"], legal_moves))

        if len(moves_with_best_score) == 1:
            if strategy == 11:
                best_move = self._strategy_with_blanks_for_one_move(legal_moves, moves_with_best_score[0], letters_bag, best_score_move)
            elif strategy == 12:
                best_move = self.get_move_with_no_imbalance(legal_moves)

        else:
            if strategy == 11:
                best_move = self.get_longest_word(moves_with_best_score)
            elif strategy == 12:
                best_move = self.get_shortest_word(moves_with_best_score)
            elif strategy == 13:
                best_move = self.get_word_with_highest_points_to_used_letters_ratio(moves_with_best_score)
            elif strategy == 14:
                best_move = self.get_word_with_lowest_points_to_used_letters_ratio(moves_with_best_score)
            elif strategy == 15:
                best_move = self.get_move_with_most_rare_letters(moves_with_best_score)
            elif strategy == 16:
                best_move = self.get_move_with_least_rare_letters(moves_with_best_score)
            elif strategy == 17:
                best_move = self.get_word_using_most_double_letters(moves_with_best_score)

        return best_move

    def get_best_move(self, strategy: int, letters_bag: "List[str]", board: "ScrabbleBoard") -> dict:
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
        elif strategy == 5:
            best_move = self.get_move_with_least_rare_letters(self.legal_moves)
        elif strategy == 6:
            best_move = self.get_rid_off_most_letters_at_the_end(self.legal_moves, letters_bag)
        elif strategy == 7:
            self.set_used_letters_from_rack(self.legal_moves, board)
            best_move = self.get_move_with_the_most_letters_from_rack(self.legal_moves)
        elif strategy == 8:
            self.set_used_letters_from_rack(self.legal_moves, board)
            best_move = self.get_move_with_least_letters_from_rack(self.legal_moves)
        elif strategy == 9:
            self.set_bonus_field_count(self.legal_moves, board)
            best_move = self.get_move_with_most_bonus_fields(self.legal_moves)
        elif strategy == 10:
            best_move = self.get_move_with_wild_card_strategy(self.legal_moves)
        elif strategy in [11, 12]:
            best_move = self.complex_strategy_1(self.legal_moves, strategy)

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
                    expanded_word = partial_word + next_letter
                    self.wild_card_idxes.append(len(expanded_word) - 1)
                    self.before_part(
                        expanded_word,
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
