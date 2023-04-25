from typing import TYPE_CHECKING
from game import Game
import csv
import game_settings


if TYPE_CHECKING:
    from typing import List


class GameStatistics:
    def __init__(self):
        self.dictionary = Game.get_dictionary()
        self.games_number = game_settings.settings.number_of_games
        self.players_number = self.games_number = game_settings.settings.number_of_players
        self.simulation_scores = []
        self.players_strategies = game_settings.settings.players_strategies
        self._games_results = []
    def simulate_single_game(self):
        game = Game(players_number=self.players_number, dictionary=self.dictionary, players_strategies=self.players_strategies)
        game.play_game()

        game_scores = []
        for player in game.players:
            game_scores.append(player.score)
        self.simulation_scores.append(game_scores)
    def simulate_games(self) -> None:
        for i in range(self.games_number):
            print(f"Game started {i+1}/{self.games_number}")
            self.simulate_single_game()

        header = [f"player_{i+1}_score" for i in range(self.players_number)]

        with open('statistics/test.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(header)

            # write multiple rows
            writer.writerows(self.simulation_scores)

game_stats = GameStatistics()
game_stats.simulate_games()
