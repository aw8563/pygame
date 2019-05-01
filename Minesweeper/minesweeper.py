import pygame
import os
import time
import math
import random

class Block():
    def __init__(self, row, col, mine):
        self.row = row
        self.col = col
        self.mine = mine
        self.revealed = False
        self.flagged = False
        self.nAdjacent = 0

    def drawBlock(self, window, grid):
        BLACK = (0,0,0)
        GRAY = (150,150,150)

        rectangle = (self.col*grid + 1, self.row*grid + 1, grid - 1.4, grid - 1.4)
        outlineRectangle = (self.col*grid, self.row*grid, grid, grid)

        pygame.draw.rect(window, BLACK, outlineRectangle)
        pygame.draw.rect(window, GRAY, rectangle)


class Game():
    def __init__(self, speed, grid, width, height, nMines):
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()
        self.clock = pygame.time.Clock()
        self.speed = speed
        self.grid = grid
        self.width = width
        self.height = height
        self.screenWidth = width * grid
        self.screenHeight = height * grid
        self.nMines = nMines

    def showBoard(self):
        for line in self.boardState:
            for cell in line:
                print(cell.nAdjacent, end = " ")
            print()

    def resetGame(self):
        self.running = True
        self.window = pygame.display.set_mode((self.screenHeight, self.screenWidth))
        pygame.display.set_caption("Minesweeper")

        # create initial board
        board = []
        for row in range(self.height):
            l = []
            for col in range(self.width):
                l.append(Block(row, col, False))
            board.append(l)

        self.boardState = board
        # add mines
        for _ in range(self.nMines):
            
            row = random.randint(0,self.height - 1)
            col = random.randint(0,self.width - 1)

            # makes sure there aren't overlaps
            while (self.boardState[row][col].mine):
                row = random.randint(0,self.height - 1)
                col = random.randint(0,self.width - 1)

            self.boardState[row][col].mine = True
            self.boardState[row][col].nAdjacent = 'X'

            # update adjacent tiles
            checks = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
            for c in checks:
                if (row + c[0] in range(0, self.height) and col + c[1] in range(0, self.width)):
                    if (not self.boardState[row + c[0]][col + c[1]].mine):
                        self.boardState[row + c[0]][col + c[1]].nAdjacent += 1


        self.showBoard()


        pass

    def refresh(self):
        self.drawBoard()
        pygame.display.update()
        self.clock.tick(self.speed)

    def drawBoard(self):
        for row in self.boardState:
            for block in row:
                block.drawBlock(self.window, self.grid)


    def updateBoard(self, x,y):
        pass
    