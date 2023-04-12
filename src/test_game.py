from typing import TYPE_CHECKING
import pygame
from game import Game

from game_board import ScrabbleBoard
if TYPE_CHECKING:
    from typing import List, Optional
    from player_model import Player


class GameDisplayManager:
    def __init__(self, board: "ScrabbleBoard", screen_width: int, screen_height: int, player_1: "Player" = None, player_2: "Player" = None):
        self.board = board
        self.player_1 = player_1
        self.player_2 = player_2
        self.screen_width = screen_width
        self.screen_height = screen_width
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.square_width = screen_height // 20
        self.square_height = screen_height // 20
        self.margin = (screen_height // 20) // 6
        self.x_offset = screen_height // 40
        self.y_offset = screen_height // 40
        self.modifier_font = pygame.font.Font(None, screen_height // 66)
        self.tile_font = pygame.font.Font(None, screen_height // 18)
        self.score_font = pygame.font.Font(None, screen_height // 32)


    def draw_start_screen(self):
        self.screen.fill((255, 255, 255))
        space_text = self.tile_font.render("Press Space to Start", True, (0, 0, 0))
        space_rect = space_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(space_text, space_rect)

    def draw_board(self):
        for y in range(15):
            for x in range(15):
                if self.board.board[x][y]:
                    letter_x_offset = 7
                    pygame.draw.rect(self.screen, (255, 215, 0), [(self.margin + self.square_width) * x + self.margin + self.x_offset,
                                                             (self.margin + self.square_height) * y + self.margin + self.y_offset,
                                                             self.square_width, self.square_height])

                    letter = self.tile_font.render(self.board.board[x][y], True, (0, 0, 0))
                    self.screen.blit(letter, ((self.margin + self.square_width) * x + self.margin + self.x_offset + letter_x_offset,
                                         (self.margin + self.square_height) * y + self.margin + self.y_offset + 7))

                    letter_score = self.modifier_font.render(str(self.board.letter_scores[self.board.board[x][y]]), True, (0, 0, 0))
                    self.screen.blit(letter_score, ((self.margin + self.square_width) * x + self.margin + self.x_offset + 31,
                                               (self.margin + self.square_height) * y + self.margin + self.y_offset + 30))

                elif self.board.bonus_squares.get((x, y)) == "TL":
                    pygame.draw.rect(self.screen, (0, 100, 200), [(self.margin + self.square_width) * x + self.margin + self.x_offset,
                                                             (self.margin + self.square_height) * y + self.margin + self.y_offset,
                                                             self.square_width, self.square_height])
                    text_top = self.modifier_font.render("TRIPLE", True, (0, 0, 0))
                    text_mid = self.modifier_font.render("LETTER", True, (0, 0, 0))
                    text_bot = self.modifier_font.render("SCORE", True, (0, 0, 0))
                    self.screen.blit(text_top, ((self.margin + self.square_width) * x + self.margin + self.x_offset + 5,
                                           (self.margin + self.square_height) * y + self.margin + self.y_offset + 7))
                    self.screen.blit(text_mid, ((self.margin + self.square_width) * x + self.margin + self.x_offset + 5,
                                           (self.margin + self.square_height) * y + self.margin + self.y_offset + 17))
                    self.screen.blit(text_bot, ((self.margin + self.square_width) * x + self.margin + self.x_offset + 5,
                                           (self.margin + self.square_height) * y + self.margin + self.y_offset + 27))

                elif self.board.bonus_squares.get((x, y)) == "DL":
                    pygame.draw.rect(self.screen, (173, 216, 230), [(self.margin + self.square_width) * x + self.margin + self.x_offset,
                                                               (self.margin + self.square_height) * y + self.margin + self.y_offset,
                                                               self.square_width, self.square_height])
                    text_top = self.modifier_font.render("DOUBLE", True, (0, 0, 0))
                    text_mid = self.modifier_font.render("LETTER", True, (0, 0, 0))
                    text_bot = self.modifier_font.render("SCORE", True, (0, 0, 0))
                    self.screen.blit(text_top, ((self.margin + self.square_width) * x + self.margin + self.x_offset + 3,
                                           (self.margin + self.square_height) * y + self.margin + self.y_offset + 7))
                    self.screen.blit(text_mid, ((self.margin + self.square_width) * x + self.margin + self.x_offset + 5,
                                           (self.margin + self.square_height) * y + self.margin + self.y_offset + 17))
                    self.screen.blit(text_bot, ((self.margin + self.square_width) * x + self.margin + self.x_offset + 5,
                                           (self.margin + self.square_height) * y + self.margin + self.y_offset + 27))

                elif self.board.bonus_squares.get((x, y)) == "DW":
                    pygame.draw.rect(self.screen, (255, 204, 203), [(self.margin + self.square_width) * x + self.margin + self.x_offset,
                                                               (self.margin + self.square_height) * y + self.margin + self.y_offset,
                                                               self.square_width, self.square_height])
                    text_top = self.modifier_font.render("DOUBLE", True, (0, 0, 0))
                    text_mid = self.modifier_font.render("WORD", True, (0, 0, 0))
                    text_bot = self.modifier_font.render("SCORE", True, (0, 0, 0))
                    self.screen.blit(text_top, ((self.margin + self.square_width) * x + self.margin + self.x_offset + 3,
                                           (self.margin + self.square_height) * y + self.margin + self.y_offset + 7))
                    self.screen.blit(text_mid, ((self.margin + self.square_width) * x + self.margin + self.x_offset + 5,
                                           (self.margin + self.square_height) * y + self.margin + self.y_offset + 17))
                    self.screen.blit(text_bot, ((self.margin + self.square_width) * x + self.margin + self.x_offset + 5,
                                           (self.margin + self.square_height) * y + self.margin + self.y_offset + 27))

                elif self.board.bonus_squares.get((x, y)) == "TW":
                    pygame.draw.rect(self.screen, (237, 28, 36), [(self.margin + self.square_width) * x + self.margin + self.x_offset,
                                                             (self.margin + self.square_height) * y + self.margin + self.y_offset,
                                                             self.square_width, self.square_height])
                    text_top = self.modifier_font.render("TRIPLE", True, (0, 0, 0))
                    text_mid = self.modifier_font.render("WORD", True, (0, 0, 0))
                    text_bot = self.modifier_font.render("SCORE", True, (0, 0, 0))
                    self.screen.blit(text_top, ((self.margin + self.square_width) * x + self.margin + self.x_offset + 5,
                                           (self.margin + self.square_height) * y + self.margin + self.y_offset + 7))
                    self.screen.blit(text_mid, ((self.margin + self.square_width) * x + self.margin + self.x_offset + 5,
                                           (self.margin + self.square_height) * y + self.margin + self.y_offset + 17))
                    self.screen.blit(text_bot, ((self.margin + self.square_width) * x + self.margin + self.x_offset + 5,
                                           (self.margin + self.square_height) * y + self.margin + self.y_offset + 27))

                else:
                    pygame.draw.rect(self.screen, (210, 180, 140), [(self.margin + self.square_width) * x + self.margin + self.x_offset,
                                                               (self.margin + self.square_height) * y + self.margin + self.y_offset,
                                                               self.square_width, self.square_height])

    def draw_rack(self):
        player_1_text = self.tile_font.render("PLayer 1", True, (255, 255, 255))
        self.screen.blit(player_1_text, ((self.margin + self.square_width) + self.margin + self.x_offset, 715))
        player_2_text = self.tile_font.render("PLayer 2", True, (255, 255, 255))
        self.screen.blit(player_2_text, ((self.margin + self.square_width) * (len(self.player_1.rack) + + 1) + self.margin + self.x_offset, 715))
        for i, letter in enumerate(self.player_1.rack):
            letter_x_offset = 7
            pygame.draw.rect(self.screen, (255, 215, 0), [(self.margin + self.square_width) * i + self.margin + self.x_offset,
                                                     750,
                                                     self.square_width, self.square_height])

            tile_letter = self.tile_font.render(letter, True, (0, 0, 0))
            self.screen.blit(tile_letter, ((self.margin + self.square_width) * i + self.margin + self.x_offset + letter_x_offset,
                                      750 + 7))

            letter_score = self.modifier_font.render(str(self.board.letter_scores[letter]), True,
                                                     (0, 0, 0))
            self.screen.blit(letter_score, ((self.margin + self.square_width) * i + self.margin + self.x_offset + 31,
                                       750 + 30))

        for i, letter in enumerate(self.player_2.rack):
            letter_x_offset = 7
            pygame.draw.rect(self.screen, (255, 215, 0), [(self.margin + self.square_width) * (len(self.player_1.rack) + i + 1) + self.margin + self.x_offset,
                                                     750,
                                                     self.square_width, self.square_height])

            tile_letter = self.tile_font.render(letter, True, (0, 0, 0))
            self.screen.blit(tile_letter, ((self.margin + self.square_width) * (len(self.player_1.rack) + i + 1) + self.margin + self.x_offset + letter_x_offset,
                                      750 + 7))

            letter_score = self.modifier_font.render(str(self.board.letter_scores[letter]), True,
                                                     (0, 0, 0))
            self.screen.blit(letter_score, ((self.margin + self.square_width) * (len(self.player_1.rack) + i + 1) + self.margin + self.x_offset + 31,
                                       750 + 30))

    def draw_score(self):
        x_start = 720
        y_start = 50
        pygame.draw.rect(self.screen, (210, 180, 140), [x_start, 25, 450, 50])
        score_title = self.score_font.render("Player 1 moves", True, (0, 0, 0))
        self.screen.blit(score_title, (x_start + 5, 25))
        score_title = self.score_font.render("Player 2 moves", True, (0, 0, 0))
        self.screen.blit(score_title, (x_start + 240, 25))
        pygame.draw.rect(self.screen, (210, 180, 140), [x_start, y_start + 25, 450, 700])
        i = 0
        for move in self.player_1.moves:
            word, score = move
            if y_start * (i + 1) > 665:
                x_start += 130
                i = 0
            word = self.score_font.render(word, True, (0, 0, 0))
            score = self.score_font.render(str(score), True, (0, 0, 0))
            self.screen.blit(word, (x_start + 5, y_start * (i + 1)))
            self.screen.blit(score, (x_start + 105, y_start * (i + 1)))

            i += .35

        total_score = self.score_font.render(f"Total Score: {self.player_1.score}", True, (0, 0, 0))
        self.screen.blit(total_score, (x_start + 5, 700))

        i = 0
        for move in self.player_2.moves:
            word, score = move
            if y_start * (i + 1) > 665:
                x_start += 130
                i = 0
            word = self.score_font.render(word, True, (0, 0, 0))
            score = self.score_font.render(str(score), True, (0, 0, 0))
            self.screen.blit(word, (x_start + 5 + 240, y_start * (i + 1)))
            self.screen.blit(score, (x_start + 105 + 240, y_start * (i + 1)))

            i += .35

        total_score = self.score_font.render(f"Total Score: {self.player_1.score}", True, (0, 0, 0))
        self.screen.blit(total_score, (x_start + 5 + 240, 700))









# Game-level variables
# screen_width = 1000
# screen_height = 800
# screen = pygame.display.set_mode((screen_width, screen_height))
# clock = pygame.time.Clock()
# square_width = 40
# square_height = 40
# margin = 3
# mouse_x = 0
# mouse_y = 0
# x_offset = 20
# y_offset = 20
# modifier_font = pygame.font.Font(None, 12)
# tile_font = pygame.font.Font(None, 45)
# score_font = pygame.font.Font(None, 25)

import time

pygame.init()

game_display_manager = GameDisplayManager(ScrabbleBoard(), 1200, 800)
game_state = "start_screen"

running=True
while running:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_state == "start_screen":
                game = Game(game_display_manager.board)
                start = time.time()
                first_player: "Player" = game.start_game()
                second_player: "Player" = game.player_2 if first_player == game.player_1 else game.player_1
                game_display_manager.player_1 = first_player
                game_display_manager.player_2 = second_player

                game_display_manager.draw_board()
                game_display_manager.draw_rack()
                game_display_manager.draw_score()
                # pygame.time.wait(75)
                game_state = "game_screen"
                continue


    if game_state == "start_screen":
        game_display_manager.draw_start_screen()
        continue


    if game_state == "game_screen":
        game_display_manager.screen.fill((0, 0, 0))

        if game.letters_bag:
            if second_player.rack:
                second_player.make_move(
                    game.dictionary,
                    game.board,
                    game.letters_bag,
                )
            if first_player.rack:
                first_player.make_move(
                    game.dictionary,
                    game.board,
                    game.letters_bag,
                )
        else:
            end = time.time()
            game_state = "end_screen"

    if game_state == "end_screen":
        print(end-start)
        game_display_manager.draw_board()
        game_display_manager.draw_rack()
        game_display_manager.draw_score()
        continue

    game_display_manager.draw_board()
    game_display_manager.draw_rack()
    game_display_manager.draw_score()
    # pygame.time.wait(75)

