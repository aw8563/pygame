from minesweeper import *
import os
import pygame
import math
import time
import random

if __name__ == '__main__':
    FPS = 30
    
    print("Please select size")
    print("  s for small: 8x8, 10 mines")
    print("  m for medium: 16x16, 40 mines")
    print("  l for large: 24x24, 99 mines")
    print("  c for custom inputs")
    
    while (True):
        mode = input()
        if (mode == 's'):
            width = 8
            height = 8
            nMines = 10

            break
        elif (mode == 'm'):
            width = 16
            height = 16
            nMines = 40

            break
        elif (mode == 'l'):
            width = 24
            height = 24
            nMines = 99

            break
        elif (mode == 'c'):
            width = input("Please enter width: ")
            while not width.isdigit():
                width = input("Please enter a number: ")

            if int(width) > 30:
                width = 30
                print('Width set to 30')


            height = input("Please enter height: ")
            while not height.isdigit():
                Height = input("Please enter a number: ")

            if int(height) > 30:
                height = 30
                print('height set to 30')

            nMines = input("Please enter number of mines: ")
            while (int(nMines) >= int(width)*int(height)):
                nMines = input("Too many mines please less than " + str(int(width)*int(height)) + ": ")

            break



        else:
            print('ERROR: Please enter valid input')








    game = Game(FPS, int(width), int(height), int(nMines))
    game.resetGame()

    while(game.running):
        # print(currentPlayer)
        # x = random.randint(0,29)
        # y = random.randint(0,29)

        # game.boardState[x][y].revealed = True
        # x = random.randint(0,29)
        # y = random.randint(0,29)
        # game.boardState[x][y].flagged = True
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False

            game.runGame(event)


        if keys[pygame.K_q]:
            game.running = False

        if keys[pygame.K_r]:
            game.resetGame()

        game.refresh()  

    # - end -
    print("Thanks for playing!")