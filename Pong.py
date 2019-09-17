import pygame
from pygame.locals import *
import sys
import random

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 450
BACK_COLOR = (25, 30, 70)
PADDLE_COLOR = (230, 250, 160)


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
        self.speed = 4
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
        if ball.pos_x < WINDOW_WIDTH/2 - self.long_side / 2:
            if ball.pos_y > self.side_paddle_y + self.long_side/2 + ball.ball_size:
                self.side_paddle_y += self.speed
            if ball.pos_y < self.side_paddle_y + self.long_side / 2 + ball.ball_size:
                self.side_paddle_y -= self.speed
            if ball.pos_x > self.horizontal_paddles_x + self.long_side/2 + ball.ball_size:
                self.horizontal_paddles_x += self.speed
            if ball.pos_x < self.horizontal_paddles_x + self.long_side / 2 + ball.ball_size:
                self.horizontal_paddles_x -= self.speed

    def set_computer(self):
        self.side_paddle_x = 20
        self.horizontal_paddles_x = WINDOW_WIDTH/4
        self.is_computer = True
        self.speed = 3


class Ball:
    def __init__(self):
        self.pos_x = WINDOW_WIDTH/2 - 10
        self.pos_y = WINDOW_HEIGHT/2 - 10
        self.ball_size = 14
        self.ball_speed = 1
        self.ball_rect = pygame.Rect(self.pos_x, self.pos_y, self.ball_size, self.ball_size)
        self.velocity = pygame.Vector2()

    def draw_ball(self, surface, ball):
        self.ball_rect = pygame.Rect(self.pos_x, self.pos_y, self.ball_size, self.ball_size)
        surface.blit(ball, self.ball_rect)

    def serve_ball(self):
        self.velocity[0] = random.randint(1, 4)
        self.velocity[1] = random.randint(-4, 4)

    def move_ball(self):
        self.pos_x += self.ball_speed * self.velocity[0]
        self.pos_y += self.ball_speed * self.velocity[1]

    def inverse_x(self):
        if self.velocity[0] > 0:
            self.pos_x -= self.ball_size
        else:
            self.pos_x += self.ball_size
        self.velocity[0] *= -1

    def inverse_y(self):
        if self.velocity[1] > 0:
            self.pos_y -= self.ball_size/2
        else:
            self.pos_y += self.ball_size/2
        self.velocity[1] *= -1

    def reset_ball(self):
        self.pos_x = WINDOW_WIDTH/2
        self.pos_y = WINDOW_HEIGHT/2


def play_pong():
    inverse_timer = 0
    pygame.init()
    clock = pygame.time.Clock()
    player = Player()
    paddle = pygame.image.load("paddle.png")
    blue_ball = pygame.image.load("ball.png")
    vertical_paddle = pygame.transform.rotate(paddle, 90)

    computer = Player()
    computer.set_computer()
    ball = Ball()
    surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    move_down = False
    move_up = False
    move_left = False
    move_right = False
    ball_served = False

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
                if event.key == K_SPACE:
                    ball.serve_ball()
                    ball_served = True
                if event.key == K_x:
                    ball.reset_ball()
                    ball_served = False

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
        player.draw_paddles(surface, paddle, vertical_paddle)
        computer.draw_paddles(surface, paddle, vertical_paddle)
        computer.move_ai(ball)

        inverse_timer += 1
        if ball_served:
            ball.move_ball()
            if ball.pos_x + 20 > WINDOW_WIDTH:
                ball.reset_ball()
                ball_served = False
            if ball.pos_x < 0:
                ball.reset_ball()
                ball_served = False
            if ball.pos_y + 20 > WINDOW_HEIGHT:
                ball.reset_ball()
                ball_served = False
            if ball.pos_y < 0:
                ball.reset_ball()
                ball_served = False
            if ball.ball_rect.colliderect(player.side_paddle):
                ball.inverse_x()
            if ball.ball_rect.colliderect(player.top_paddle) or ball.ball_rect.colliderect(player.bottom_paddle):
                ball.inverse_y()
            if ball.ball_rect.colliderect(computer.side_paddle):
                ball.inverse_x()
            if ball.ball_rect.colliderect(computer.top_paddle) or ball.ball_rect.colliderect(computer.bottom_paddle):
                ball.inverse_y()
        ball.draw_ball(surface, blue_ball)
        pygame.display.update()
        clock.tick(120)


play_pong()
