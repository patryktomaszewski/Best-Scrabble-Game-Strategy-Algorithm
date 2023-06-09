from typing import TYPE_CHECKING
import pygame
import time

from games_statistics_provider import GameStatisticsManager
from test_game import GameDisplayManager
from game import GameManager
from game_board import ScrabbleBoard
from game_settings import settings

if TYPE_CHECKING:
    from typing import Union, Type


class GameSimulation:

    def __init__(self):
        self.game_simulation_manager: Type[GameDisplayManager] | Type[GameManager] = GameDisplayManager if settings.use_gui else GameManager
        self.game_statistics_manager = GameStatisticsManager()
        self.dictionary = self.game_simulation_manager.get_dictionary()

    def simulate_single_game(self, game_number: int):
        game = self.game_simulation_manager(dictionary=self.dictionary)
        game.play_game()

        if settings.save_game_results:
            self.game_statistics_manager.aquire_data_after_game(game, game_number)

    def run_simulation(self):

        for i in range(settings.number_of_games):
            print(f"Game started {i+1}/{settings.number_of_games}")
            self.simulate_single_game(i)
        if settings.save_game_results:
            self.game_statistics_manager.save_statistics()

GameSimulation().run_simulation()
