from aiGame import *
import pygame
import math
import os


if __name__ == '__main__':

    WIDTH = 500
    HEIGHT = 500
    game = Game(WIDTH, HEIGHT)
    game.resetGame()

    while(game.running):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            game.handleEvent(event)


        key = None
        if keys[pygame.K_q]:
            key = 'QUIT'
        if keys[pygame.K_r]:
            key = 'RESTART'

        if keys[pygame.K_RIGHT]:
            key = 1

        if keys[pygame.K_LEFT]:
            key = 0

        game.handleAction(key)
        game.runGame()
        game.refresh()  
