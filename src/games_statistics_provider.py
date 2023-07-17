from game_manager import GameManager
import csv
from game_settings import settings


class GameStatisticsManager:
    def __init__(self):
        self.simulation_scores = []
        self.simulation_words_scores = []
        self.course_of_the_game = []
        self.players_strategies = settings.players_strategies
        self._games_results = []

    def acquire_data_after_game(self, game: GameManager, game_number: int):
        game_scores = []

        for game_move in game.course_of_the_game:
            self.course_of_the_game.append(
                [game_number, f"player {game_move[0] + 1}", game_move[1]["start_pos"], game_move[1]["direction"],
                 game_move[1]["word"], game_move[1]["score"]])
        players_sorted_by_strategies = sorted(game.players, key=lambda x: x.strategy, reverse=False)
        for idx, player in enumerate(players_sorted_by_strategies):
            game_scores.append(player.score)
            for move in player.moves:
                self.simulation_words_scores.append([move[0], move[1]])
        self.simulation_scores.append(game_scores)

    def save_statistics(self) -> None:
        players_scores_header = [f"player_{i+1}_score" for i in range(settings.number_of_players)]

        players_words_scores_header = []
        for i in range(settings.number_of_players):
            players_words_scores_header.append(f"player_{i + 1}_words")

        with open('src/statistics/players_scores_1_6_10_11.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(players_scores_header)

            # write multiple rows
            writer.writerows(self.simulation_scores)

        players_words_scores_header = ["played_word", "word_score"]
        with open('src/statistics/words_scores_1_6_10_11.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(players_words_scores_header)

            # write multiple rows
            writer.writerows(self.simulation_words_scores)

        course_of_the_game_header = ["game_number", "player", "start_pos", "direction", "word", "score"]
        with open('src/statistics/course_of_the_game_1_6_10_11.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(course_of_the_game_header)

            # write multiple rows
            writer.writerows(self.course_of_the_game)
