from typing import TYPE_CHECKING
from game import GameManager
import csv
from  game_settings import settings


if TYPE_CHECKING:
    from typing import List


class GameStatisticsManager:
    def __init__(self):
        self.simulation_scores = []
        self.simulation_words_scores = []
        self.course_of_the_game = []
        self.players_strategies = settings.players_strategies
        self._games_results = []

    def aquire_data_after_game(self, game: GameManager, game_number: int):
        game_scores = []

        for game_move in game.course_of_the_game:
            self.course_of_the_game.append(
                [game_number, f"player {game_move[0]}", game_move[1]["start_pos"], game_move[1]["direction"],
                 game_move[1]["word"], game_move[1]["score"]])

        for idx, player in enumerate(game.players):
            game_scores.append(player.score)
            for move in player.moves:
                self.simulation_words_scores.append([move[0], move[1]])
        self.simulation_scores.append(game_scores)


    def save_statistics(self) -> None:
        players_scores_header = [f"player_{i+1}_score" for i in range(settings.number_of_players)]

        players_words_scores_header = []
        for i in range(settings.number_of_players):
            players_words_scores_header.append(f"player_{i + 1}_words")

        with open('statistics/test.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(players_scores_header)

            # write multiple rows
            writer.writerows(self.simulation_scores)

        players_words_scores_header = ["played_word", "word_score"]
        with open('statistics/words_scores_test.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(players_words_scores_header)

            # write multiple rows
            writer.writerows(self.simulation_words_scores)

        course_of_the_game_header = ["game_number", "player", "start_pos", "direction", "word", "score"]
        with open('statistics/course_of_the_game_test.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(course_of_the_game_header)

            # write multiple rows
            writer.writerows(self.course_of_the_game)
