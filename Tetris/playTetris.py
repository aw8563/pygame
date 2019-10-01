from tetris import Game as game
import pygame

g = game(15)

g.resetGame()


alternate = False
while g.running:
    if (alternate == False):
        alternate = True
    else:
        alternate = False

    g.runGame(alternate)
    g.refresh()
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            g.running = False
            break
    if key[pygame.K_q]:
        g.running = False
    if key[pygame.K_r]:
        g.resetGame()