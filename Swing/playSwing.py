#!/usr/bin/python3

import time
import math
import os
import pygame

from swing import *


# default game settings
FPS = 20
WIDTH = 500
HEIGHT = 500

if __name__ == '__main__':
    game = Game(FPS, WIDTH, HEIGHT) # setup game
    game.resetGame()

    while (game.running):

        if (game.debug):
            print("debugging")
            if (input() != ""):
                game.debug = False
        game.getAction()
        game.runGame()
        game.refresh()


