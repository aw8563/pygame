from minesweeper import *
import os
import pygame
import math
import time


FPS = 30
grid = 10

game = Game(FPS,grid, 50,50, 50)
game.resetGame()


while(game.running):
    # print(currentPlayer)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False

    if keys[pygame.K_q]:
        game.running = False

    if keys[pygame.K_r]:
        game.resetGame()

    game.refresh()    

# - end -
