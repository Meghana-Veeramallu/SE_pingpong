import pygame
from game.game_engine import GameEngine

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Game")

clock = pygame.time.Clock()
game = GameEngine(WIDTH, HEIGHT)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # After game over, wait for user keypress to show menu
        elif event.type == pygame.KEYDOWN and game.game_over:
            game.show_replay_menu()

        # Handle replay menu choices
        elif event.type == pygame.KEYDOWN and game.show_menu:
            if event.key == pygame.K_3:
                game.reset_game(3)
            elif event.key == pygame.K_5:
                game.reset_game(5)
            elif event.key == pygame.K_7:
                game.reset_game(7)
            elif event.key == pygame.K_ESCAPE:
                running = False

    # Regular gameplay
    if not game.show_menu:
        game.handle_input()
        game.update()

    game.render(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
