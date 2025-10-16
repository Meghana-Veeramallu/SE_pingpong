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

    game.handle_input()
    game.update()
    game.render(screen)
    pygame.display.flip()

    # If game over, delay and exit gracefully
    if game.game_over:
        pygame.display.flip()
        pygame.time.delay(3000)  # 3-second delay before exit
        running = False

    clock.tick(60)

pygame.quit()
