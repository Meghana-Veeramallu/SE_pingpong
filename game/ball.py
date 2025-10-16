import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
        self.hit_sound = pygame.mixer.Sound("assets/paddle_hit.wav")
        self.wall_sound = pygame.mixer.Sound("assets/wall_bounce.wav")
        self.score_sound = pygame.mixer.Sound("assets/score.wav")

    def move(self):
        # Move the ball in small increments for more accurate collision
        steps = max(abs(self.velocity_x), abs(self.velocity_y))
        for _ in range(steps):
            self.x += self.velocity_x / steps
            self.y += self.velocity_y / steps

            # Bounce on walls
            if self.y <= 0 or self.y + self.height >= self.screen_height:
                self.velocity_y *= -1
                self.wall_sound.play()
                break

    def check_collision(self, player, ai):
        ball_rect = self.rect()
        if ball_rect.colliderect(player.rect()):
            self.x = player.x + player.width
            self.velocity_x = abs(self.velocity_x)
            self.hit_sound.play()

        elif ball_rect.colliderect(ai.rect()):
            self.x = ai.x - self.width
            self.velocity_x = -abs(self.velocity_x)
            self.hit_sound.play()

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)