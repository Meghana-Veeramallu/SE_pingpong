import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over = False
        self.winner = None

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)

        # Game over condition
        if self.player_score >= 5:
            self.game_over = True
            self.winner = "Player"
        elif self.ai_score >= 5:
            self.game_over = True
            self.winner = "AI"

    def display_game_over(self, screen):
        font = pygame.font.SysFont("Arial", 60)
        text = f"{self.winner} Wins!"
        label = font.render(text, True, (255, 255, 255))
        screen.fill((0, 0, 0))
        screen.blit(label, (self.width//2 - 150, self.height//2 - 50))
        pygame.display.flip()

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    
    def display_replay_menu(self, screen):
        font = pygame.font.SysFont("Arial", 30)
        options = [
            "Press 3 for Best of 3",
            "Press 5 for Best of 5",
            "Press 7 for Best of 7",
            "Press ESC to Exit"
        ]
        screen.fill((0, 0, 0))
        for i, text in enumerate(options):
            label = font.render(text, True, (255, 255, 255))
            screen.blit(label, (self.width//2 - 150, 200 + i*50))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        return 3
                    elif event.key == pygame.K_5:
                        return 5
                    elif event.key == pygame.K_7:
                        return 7
                    elif event.key == pygame.K_ESCAPE:
                        return None
                
    def reset_game(self, target_score):
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.winner = None
        self.target_score = target_score
        self.ball.reset()