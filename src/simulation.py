from typing import TYPE_CHECKING

from games_statistics_provider import GameStatisticsManager
from game_display_manager import GameDisplayManager
from game_manager import GameManager
from game_settings import settings

if TYPE_CHECKING:
    from typing import Type


class GameSimulation:

    def __init__(self):
        self.game_simulation_manager: Type[GameDisplayManager] | Type[
            GameManager] = GameDisplayManager if settings.use_gui else GameManager
        self.game_statistics_manager = GameStatisticsManager()
        self.dictionary = self.game_simulation_manager.get_dictionary()

    def simulate_single_game(self, game_number: int, strategies):
        game = self.game_simulation_manager(dictionary=self.dictionary, players_strategies=strategies)
        game.play_game()

        if settings.save_game_results:
            self.game_statistics_manager.acquire_data_after_game(game, game_number)

    def run_simulation(self):
        strategies_reorder_idx = 0
        for i in range(settings.number_of_games):
            strategies = settings.players_strategies[strategies_reorder_idx:] + settings.players_strategies[:strategies_reorder_idx]
            print(f"Game started {i+1}/{settings.number_of_games}")
            self.simulate_single_game(i, strategies)
            strategies_reorder_idx += 1
            if strategies_reorder_idx == 4:
                strategies_reorder_idx = 0
        if settings.save_game_results:
            self.game_statistics_manager.save_statistics()

GameSimulation().run_simulation()
