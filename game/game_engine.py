import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.font = pygame.font.SysFont("Arial", 30)
        self.large_font = pygame.font.SysFont("Arial", 40)

        # Default settings
        self.player_score = 0
        self.ai_score = 0
        self.target_score = 5  # default: best of 5
        self.game_over = False
        self.show_menu = False
        self.winner_text = ""

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        if self.game_over or self.show_menu:
            return  # pause updates when game is over or menu is open

        self.ball.move(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)
        self.check_game_over()

    def check_game_over(self):
        """Check if anyone reached the target score."""
        if self.player_score == self.target_score:
            self.winner_text = "Player Wins!"
            self.game_over = True
        elif self.ai_score == self.target_score:
            self.winner_text = "AI Wins!"
            self.game_over = True

    def render(self, screen):
        screen.fill(BLACK)

        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Draw scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

        # Game Over screen
        if self.game_over:
            text_surface = self.large_font.render(self.winner_text, True, WHITE)
            screen.blit(text_surface, (self.width // 2 - text_surface.get_width() // 2, self.height // 2 - 60))

            hint = self.font.render("Press any key to continue...", True, WHITE)
            screen.blit(hint, (self.width // 2 - hint.get_width() // 2, self.height // 2 + 10))

        # Replay menu
        if self.show_menu:
            title = self.large_font.render("Choose Game Mode", True, WHITE)
            screen.blit(title, (self.width // 2 - title.get_width() // 2, self.height // 2 - 120))

            opt1 = self.font.render("3 - Best of 3", True, WHITE)
            opt2 = self.font.render("5 - Best of 5", True, WHITE)
            opt3 = self.font.render("7 - Best of 7", True, WHITE)
            opt4 = self.font.render("ESC - Exit", True, WHITE)

            screen.blit(opt1, (self.width // 2 - opt1.get_width() // 2, self.height // 2 - 40))
            screen.blit(opt2, (self.width // 2 - opt2.get_width() // 2, self.height // 2))
            screen.blit(opt3, (self.width // 2 - opt3.get_width() // 2, self.height // 2 + 40))
            screen.blit(opt4, (self.width // 2 - opt4.get_width() // 2, self.height // 2 + 80))

    def show_replay_menu(self):
        """Prepare to show replay menu."""
        self.show_menu = True
        self.game_over = False

    def reset_game(self, target_score):
        """Reset all scores and positions for replay."""
        self.player_score = 0
        self.ai_score = 0
        self.target_score = target_score
        self.ball.reset()
        self.game_over = False
        self.show_menu = False
