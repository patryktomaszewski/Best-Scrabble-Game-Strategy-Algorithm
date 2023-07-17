from typing import TYPE_CHECKING
import pygame
from game_manager import GameManager
import time
from game_settings import settings

if TYPE_CHECKING:
    from typing import Optional
    from dawg_graph import DAWG


class GameDisplayManager(GameManager):

    def __init__(self, dictionary: "DAWG" = None, screen_width: "Optional[int]" = 1400, screen_height: "Optional[int]" = 800):
        super().__init__(dictionary=dictionary)
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.square_width = screen_height // 21
        self.square_height = screen_height // 21
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
        rack_offset = 50
        start_position = 0
        end_position = 0
        for i, player in enumerate(self.players):
            player_text = self.tile_font.render(f"PLayer {i + 1}", True, (255, 255, 255))
            self.screen.blit(player_text, (self.margin + self.x_offset + end_position, 715))

            for k, letter in enumerate(player.rack):
                letter_x_offset = 7
                x_position = (self.margin + self.square_width) * k + self.margin + self.x_offset + end_position
                pygame.draw.rect(self.screen, (255, 215, 0), [
                    x_position,
                    750,
                    self.square_width, self.square_height])

                tile_letter = self.tile_font.render(letter, True, (0, 0, 0))
                self.screen.blit(tile_letter, (x_position + letter_x_offset,
                                               750 + 7))

                letter_score = self.modifier_font.render(str(self.board.letter_scores[letter]), True,
                                                         (0, 0, 0))
                self.screen.blit(letter_score, (x_position + 31,
                                                750 + 30))

            end_position = x_position + rack_offset



    def draw_score(self):
        x_start = 720
        y_start = 25
        pygame.draw.rect(self.screen, (210, 180, 140), [x_start, y_start, 650, 680])
        for i, player in enumerate(self.players):
            score_title = self.score_font.render(f"Player {i + 1} score", True, (0, 0, 0))
            self.screen.blit(score_title, (x_start + 20 + (450//4 + 40) * i, y_start + 25))

            k = 0
            for move in player.moves:
                word, score = move
                if y_start * (k + 1) > 665:
                    x_start += 130
                    k = 0
                word = self.score_font.render(word, True, (0, 0, 0))
                score = self.score_font.render(str(score), True, (0, 0, 0))
                self.screen.blit(word, (x_start + 20 + (450//4 + 40) * i, (y_start + 45) * (k + 1)))
                self.screen.blit(score, (x_start + 120 + (450//4 + 40) * i, (y_start + 45) * (k + 1)))

                k += .35

            total_score = self.score_font.render(f"Total Score: {player.score}", True, (0, 0, 0))
            self.screen.blit(total_score, (x_start + 20 + (450//4 + 40) * i, 650))

    def play_game(self):
        game_state = "start_screen"

        running = True
        while running:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and game_state == "start_screen":
                        idx, first_player = self.start_game()
                        for idx, player in enumerate(self.players[idx:], idx):
                            move_made = player.make_move(
                                self.dictionary,
                                self.board,
                                self.letters_bag,
                            )
                            self.update_course_of_the_game_if_move_made(move_made, idx)

                        self.draw_board()
                        self.draw_rack()
                        self.draw_score()
                        # pygame.time.wait(75)
                        game_state = "game_screen"
                        continue

            if game_state == "start_screen":
                self.draw_start_screen()
                continue

            if game_state == "game_screen":
                self.screen.fill((0, 0, 0))

                if self.letters_bag:
                    for idx, player in enumerate(self.players):
                        move_made = player.make_move(
                            self.dictionary,
                            self.board,
                            self.letters_bag,
                        )
                        self.update_course_of_the_game_if_move_made(move_made, idx)

                else:
                    game_state = "end_screen"
                    time.sleep(4)
                    running = False

            if game_state == "end_screen":
                self.draw_board()
                self.draw_rack()
                self.draw_score()
                continue

            self.draw_board()
            self.draw_rack()
            self.draw_score()

    def simulate_games(self) -> None:
        for i in range(settings.number_of_games):
            self.play_game()
