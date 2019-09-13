import time
import math
import os
import pygame
import random

from snake import *


# default game settings
FPS = 30
WIDTH = 40
HEIGHT = 40

if __name__ == '__main__':
    game = Game(FPS, WIDTH, HEIGHT) # setup game
    game.resetGame()

    while (game.running):
        game.getAction()
        game.runGame()
        game.refresh()

        if (game.gameOver):
        	game.resetGame()


