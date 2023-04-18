from typing import TYPE_CHECKING
from game import Game
import csv

if TYPE_CHECKING:
    from typing import List


class GameStatistics:
    def __init__(self, games_number: int, players_number: int, players_strategies: "List[int]" = None):
        self.games_number = games_number
        self.dictionary = Game.get_dictionary()
        self.games_number = games_number
        self.players_number = players_number
        self.simulation_scores = []
        self.players_strategies = players_strategies
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

        with open('simulations_scores_rules_1_2_3_4_players.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(header)

            # write multiple rows
            writer.writerows(self.simulation_scores)


game_stats = GameStatistics(1000, 4, [1, 2, 3, 4])
game_stats.simulate_games()
