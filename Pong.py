import pygame
from pygame.locals import *
import sys
import random

# Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 550
BACK_COLOR = (25, 30, 70)
WHITE = (250, 250, 250)
GREEN = (117, 240, 142)


class Player:
    def __init__(self):
        self.is_computer = False
        self.side_paddle_x = WINDOW_WIDTH - 40
        self.side_paddle_y = 200
        self.horizontal_paddles_x = WINDOW_WIDTH - (WINDOW_WIDTH/4)
        self.top_paddle_y = 20
        self.bottom_paddle_y = WINDOW_HEIGHT - 40
        self.long_side = 120
        self.short_side = 20
        self.speed = 7
        self.side_paddle = pygame.Rect(self.side_paddle_x, self.side_paddle_y, self.short_side, self.long_side)
        self.top_paddle = pygame.Rect(self.horizontal_paddles_x, self.top_paddle_y, self.long_side, self.short_side)
        self.bottom_paddle = pygame.Rect(
            self.horizontal_paddles_x, self.bottom_paddle_y, self.long_side, self.short_side)

    def draw_paddles(self, surface, horizontal, vertical):
        self.side_paddle = pygame.Rect(self.side_paddle_x, self.side_paddle_y, self.short_side, self.long_side)
        self.top_paddle = pygame.Rect(self.horizontal_paddles_x, self.top_paddle_y, self.long_side, self.short_side)
        self.bottom_paddle = pygame.Rect(
            self.horizontal_paddles_x, self.bottom_paddle_y, self.long_side, self.short_side)

        surface.blit(vertical, self.side_paddle)
        surface.blit(horizontal, self.top_paddle)
        surface.blit(horizontal, self.bottom_paddle)

    def move_side_paddle(self, y_direction):
        if y_direction == "down":
            self.side_paddle_y += self.speed
        if y_direction == "up":
            self.side_paddle_y -= self.speed

    def move_horizontal_paddles(self, x_direction):
        if x_direction == "left":
            self.horizontal_paddles_x -= self.speed
        if x_direction == "right":
            self.horizontal_paddles_x += self.speed

    def move_ai(self, ball):
        # The computer vertical paddle only sees up to 75% of length of screen
        if ball.pos_y > (self.side_paddle_y + self.long_side / 2) - ball.ball_size/2:
            self.side_paddle_y += self.speed
        if ball.pos_y < (self.side_paddle_y + self.long_side / 2) + ball.ball_size/2:
            self.side_paddle_y -= self.speed
        offset = WINDOW_WIDTH/2 - self.long_side
        if ball.pos_x > self.horizontal_paddles_x + self.long_side / 2 and self.horizontal_paddles_x < offset:
            self.horizontal_paddles_x += self.speed
        if ball.pos_x < self.horizontal_paddles_x + self.long_side / 2:
            self.horizontal_paddles_x -= self.speed

    def set_computer(self):
        self.side_paddle_x = 20
        self.horizontal_paddles_x = WINDOW_WIDTH/4
        self.is_computer = True
        self.speed = 3.5


class Ball:
    def __init__(self):
        self.ball_size = 14
        self.ball_speed = 1
        self.pos_x = WINDOW_WIDTH/2 - self.ball_size/2
        self.pos_y = WINDOW_HEIGHT/2 - self.ball_size/2
        self.x_random_speed = random.randint(2, 4)
        self.y_random_speed = 1
        self.ball_rect = pygame.Rect(self.pos_x, self.pos_y, self.ball_size, self.ball_size)
        self.velocity = pygame.Vector2()

    def draw_ball(self, surface, ball):
        self.ball_rect = pygame.Rect(self.pos_x, self.pos_y, self.ball_size, self.ball_size)
        surface.blit(ball, self.ball_rect)

    def serve_ball(self, direction):
        self.x_random_speed = random.randint(4, 6)
        self.y_random_speed = random.randint(2, 4)
        if direction == 'computer':
            x_direction = -1
        else:
            x_direction = 1
        y_direction = random.randint(0, 1)
        self.velocity[1] = self.y_random_speed if y_direction == 0 else -self.y_random_speed
        if x_direction == 1:
            self.velocity[0] = self.x_random_speed
        else:
            self.velocity[0] = -self.x_random_speed

    def move_ball(self):
        self.pos_x += self.velocity[0] * self.ball_speed
        self.pos_y += self.velocity[1] * self.ball_speed

    def inverse_x(self):
        self.velocity[0] *= -1

    def inverse_y(self):
        self.velocity[1] *= -1

    def reset_ball(self):
        self.pos_x = WINDOW_WIDTH/2 - self.ball_size/2
        self.pos_y = WINDOW_HEIGHT/2 - self.ball_size/2


class Scores:
    def __init__(self):
        self.player_score = 0
        self.ai_score = 0
        self.player_matches_won = 0
        self.ai_matches_won = 0
        self.needed_points = 11
        self.needed_games = 3
        self.player_is_winner = False
        self.ai_is_winner = False
        self.lose_point_sound = pygame.mixer.Sound("sounds/lose_point.wav")
        self.lose_match_sound = pygame.mixer.Sound("sounds/lose_match.wav")
        self.lose_game_sound = pygame.mixer.Sound("sounds/lose_game.wav")
        self.win_point_sound = pygame.mixer.Sound("sounds/win_point.wav")
        self.win_match_sound = pygame.mixer.Sound("sounds/win_match.wav")
        self.win_game_sound = pygame.mixer.Sound("sounds/win_game.wav")

    def draw_score(self, surface):
        score_font = pygame.font.Font('fonts/slkscr.ttf', 92)
        player_text = score_font.render("{}".format(self.player_score), 1, WHITE)
        player_rect = player_text.get_rect()
        player_rect.topleft = WINDOW_WIDTH/2 + 40, 40
        surface.blit(player_text, player_rect)
        ai_text = score_font.render("{}".format(self.ai_score), 1, WHITE)
        ai_rect = ai_text.get_rect()
        ai_rect.topright = WINDOW_WIDTH/2 - 40, 40
        surface.blit(ai_text, ai_rect)
        game_won_font = pygame.font.Font('fonts/slkscr.ttf', 45)
        game_undecided_font = pygame.font.Font('fonts/slkscr.ttf', 30)
        indicator = "O"
        player_wins = self.player_matches_won
        computer_wins = self.ai_matches_won
        for i in range(3):
            # Player Matches
            offset = 0
            if player_wins > 0:
                player_wins -= 1
                indicator_text = game_won_font.render(indicator, 1, GREEN)
                offset = 4
            else:
                indicator_text = game_undecided_font.render(indicator, 1, WHITE)
            indicator_rect = indicator_text.get_rect()
            indicator_rect.bottomleft = ((WINDOW_WIDTH/2 + 50) + (i * 40),  170 + offset)
            surface.blit(indicator_text, indicator_rect)
            # Computer Matches
            offset = 0
            if computer_wins > 0:
                computer_wins -= 1
                indicator_ai_text = game_won_font.render(indicator, 1, GREEN)
                offset = 4
            else:
                indicator_ai_text = game_undecided_font.render(indicator, 1, WHITE)
            indicator_ai_rect = indicator_ai_text.get_rect()
            indicator_ai_rect.bottomright = ((WINDOW_WIDTH/2 - 50) - (i * 40),  170 + offset)
            surface.blit(indicator_ai_text, indicator_ai_rect)

    def increase_scores(self, ball):
        if ball.pos_x + ball.ball_size > WINDOW_WIDTH:
            self.ai_score += 1
            self.lose_point_sound.play()
            ball.reset_ball()
            ball.serve_ball('computer')
        if ball.pos_x < 0:
            self.player_score += 1
            self.win_point_sound.play()
            ball.reset_ball()
            ball.serve_ball('player')
        # Ball hits the bottom
        if ball.pos_y + ball.ball_size > WINDOW_HEIGHT:
            if ball.pos_x > WINDOW_WIDTH/2:
                self.ai_score += 1
                self.lose_point_sound.play()
                ball.reset_ball()
                ball.serve_ball('computer')
            else:
                self.player_score += 1
                self.win_point_sound.play()
                ball.reset_ball()
                ball.serve_ball('player')
            ball.reset_ball()
        if ball.pos_y < 0:
            if ball.pos_x < WINDOW_WIDTH/2:
                self.player_score += 1
                self.win_point_sound.play()
                ball.reset_ball()
                ball.serve_ball('player')
            else:
                self.ai_score += 1
                self.lose_point_sound.play()
                ball.reset_ball()
                ball.serve_ball('computer')

    def check_scores(self, ball):
        if self.player_score > self.ai_score:
            difference = self.player_score - self.ai_score
            if self.player_score >= self.needed_points and difference > 1:
                self.player_score = 0
                self.ai_score = 0
                self.player_matches_won += 1
                if self.player_matches_won == self.needed_games:
                    self.player_score = 0
                    self.ai_score = 0
                    self.player_matches_won = 0
                    self.ai_matches_won = 0
                    self.win_match_sound.play()
                    self.player_is_winner = True
                    ball.reset_ball()
                else:
                    self.win_game_sound.play()

        if self.ai_score > self.player_score:
            difference = self.ai_score - self.player_score
            if self.ai_score >= self.needed_points and difference > 1:
                self.player_score = 0
                self.ai_score = 0
                self.ai_matches_won += 1
                if self.ai_matches_won == self.needed_games:
                    self.player_score = 0
                    self.ai_score = 0
                    self.player_matches_won = 0
                    self.ai_matches_won = 0
                    self.lose_match_sound.play()
                    self.ai_is_winner = True
                    ball.reset_ball()
                else:
                    self.lose_game_sound.play()

    def reset_winner(self):
        self.ai_is_winner = False
        self.player_is_winner = False


def draw_net(surface):
    dashes = WINDOW_HEIGHT / 15
    x_counter = 10
    for x in range(15):
        pygame.draw.line(surface, (255, 255, 255), (WINDOW_WIDTH / 2, x_counter), (WINDOW_WIDTH / 2, x_counter + 20), 5)
        x_counter += dashes


def draw_main_screen(surface):
    surface.fill(BACK_COLOR)
    # Title
    title_font = pygame.font.Font('fonts/slkscr.ttf', 82)
    title_text = title_font.render("Pong", 1, WHITE)
    title_rect = title_text.get_rect()
    title_width = title_rect.topright[0] - title_rect.topleft[0]
    title_rect.topleft = WINDOW_WIDTH / 2 - title_width/2, 60
    surface.blit(title_text, title_rect)

    # Tip
    tip_font = pygame.font.Font('fonts/slkscr.ttf', 16)
    tip_text = tip_font.render(
        "Tip: Hitting the ball with the tips of the vertical paddle makes it go faster.", 1, WHITE)
    tip_rect = tip_text.get_rect()
    tip_width = tip_rect.topright[0] - tip_rect.topleft[0]
    tip_rect.topleft = WINDOW_WIDTH / 2 - tip_width/2, WINDOW_HEIGHT - 200
    surface.blit(tip_text, tip_rect)

    # Press to start
    start_font = pygame.font.Font('fonts/slkscr.ttf', 32)
    start_text = start_font.render("Press Space to Start", 1, WHITE)
    start_rect = start_text.get_rect()
    width = start_rect.topright[0] - start_rect.topleft[0]
    start_rect.topleft = WINDOW_WIDTH / 2 - width/2, WINDOW_HEIGHT - 60
    surface.blit(start_text, start_rect)


def draw_player_wins(surface):
    player_win_font = pygame.font.Font('fonts/slkscr.ttf', 54)
    player_win_text = player_win_font.render("Player Wins!", 1, WHITE)
    player_win_rect = player_win_text.get_rect()
    player_win_width = player_win_rect.topright[0] - player_win_rect.topleft[0]
    player_win_rect.topleft = WINDOW_WIDTH * 0.75 - player_win_width/2, 60
    surface.blit(player_win_text, player_win_rect)

    rematch_font = pygame.font.Font('fonts/slkscr.ttf', 26)
    rematch_text = rematch_font.render("Press SPACE to play again.", 1, WHITE)
    rematch_rect = rematch_text.get_rect()
    rematch_width = rematch_rect.topright[0] - rematch_rect.topleft[0]
    rematch_rect.topleft = WINDOW_WIDTH * 0.75 - rematch_width/2, 160
    surface.blit(rematch_text, rematch_rect)


def draw_ai_wins(surface):
    ai_win_font = pygame.font.Font('fonts/slkscr.ttf', 44)
    ai_win_text = ai_win_font.render("Computer Wins", 1, WHITE)
    ai_win_rect = ai_win_text.get_rect()
    ai_win_width = ai_win_rect.topright[0] - ai_win_rect.topleft[0]
    ai_win_rect.topleft = WINDOW_WIDTH * 0.25 - ai_win_width/2, 60
    surface.blit(ai_win_text, ai_win_rect)

    rematch_font = pygame.font.Font('fonts/slkscr.ttf', 26)
    rematch_text = rematch_font.render("Press SPACE to play again.", 1, WHITE)
    rematch_rect = rematch_text.get_rect()
    rematch_width = rematch_rect.topright[0] - rematch_rect.topleft[0]
    rematch_rect.topleft = WINDOW_WIDTH * 0.25 - rematch_width/2, 160
    surface.blit(rematch_text, rematch_rect)


def check_for_input():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return True


def play_pong():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    pygame.init()

    clock = pygame.time.Clock()
    paddle = pygame.image.load("images/paddle.png")
    game_ball = pygame.image.load("images/ball.png")
    vertical_paddle = pygame.transform.rotate(paddle, 90)
    bounce_sound = pygame.mixer.Sound("sounds/bounce.wav")

    player = Player()
    points = Scores()
    computer = Player()
    computer.set_computer()
    ball = Ball()

    surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    move_down = False
    move_up = False
    move_left = False
    move_right = False
    start_game = False

    while not start_game:
        draw_main_screen(surface)
        pygame.display.update()
        start_game = check_for_input()
    ball.serve_ball('player')

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    move_down = True
                    move_up = False
                if event.key == K_UP:
                    move_up = True
                    move_down = False
                if event.key == K_LEFT:
                    move_right = False
                    move_left = True
                if event.key == K_RIGHT:
                    move_left = False
                    move_right = True

            if event.type == KEYUP:
                if event.key == K_DOWN:
                    move_down = False
                if event.key == K_UP:
                    move_up = False
                if event.key == K_LEFT:
                    move_left = False
                if event.key == K_RIGHT:
                    move_right = False

        if move_down and player.side_paddle_y + player.long_side < WINDOW_HEIGHT:
            player.move_side_paddle("down")
        if move_up and player.side_paddle_y > 0:
            player.move_side_paddle("up")
        if move_left and player.horizontal_paddles_x > WINDOW_WIDTH/2:
            player.move_horizontal_paddles("left")
        if move_right and player.horizontal_paddles_x + player.long_side < WINDOW_WIDTH:
            player.move_horizontal_paddles("right")

        surface.fill(BACK_COLOR)
        draw_net(surface)
        player.draw_paddles(surface, paddle, vertical_paddle)
        computer.draw_paddles(surface, paddle, vertical_paddle)
        computer.move_ai(ball)
        points.increase_scores(ball)

        if points.player_is_winner or points.ai_is_winner:
            restart_game = False
            while not restart_game:
                if points.player_is_winner:
                    draw_player_wins(surface)
                else:
                    draw_ai_wins(surface)
                pygame.display.update()
                restart_game = check_for_input()
                points.reset_winner()
        points.check_scores(ball)
        ball.move_ball()

        if ball.ball_rect.colliderect(player.side_paddle):
            ball.inverse_x()
            # Equation to calculate Angle: ball.middle - paddle.top + 60 = relative position
            # Relative position * (8/60) = y speed and direction
            relative_position = (ball.ball_rect.top + ball.ball_size/2) - (player.side_paddle.top + 60)
            ball.velocity[1] = relative_position * (8/60)
            ball.pos_x = player.side_paddle.left - ball.ball_size
            bounce_sound.play()
        if ball.ball_rect.colliderect(computer.side_paddle):
            ball.inverse_x()
            ball.pos_x = computer.side_paddle.right + ball.ball_size
            bounce_sound.play()
        if ball.ball_rect.colliderect(player.top_paddle) or ball.ball_rect.colliderect(computer.top_paddle):
            ball.inverse_y()
            ball.pos_y = player.top_paddle.bottom + ball.ball_size
            bounce_sound.play()
        if ball.ball_rect.colliderect(player.bottom_paddle) or ball.ball_rect.colliderect(computer.bottom_paddle):
            ball.inverse_y()
            ball.pos_y = player.bottom_paddle.top - ball.ball_size
            bounce_sound.play()
        ball.draw_ball(surface, game_ball)
        points.draw_score(surface)

        pygame.display.update()
        clock.tick(60)


play_pong()
