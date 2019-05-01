import pygame
import os
import math
import time
from abc import ABC, abstractmethod

WHITE = (200,200,200)
BROWN = (100,100,100)


class Piece():

    def __init__(self, grid, colour, pieceType, x, y):
        self.colour = colour # W or B
        self.pieceType = pieceType # Bishop, Knight etc
        self.coord = [x,y] # [A,1], [C,3] .. etc
        self.grid = grid
        xy = self.getXY()

        self.x = xy[0]
        self.y = xy[1]
        self.image = pygame.image.load(self.getName())


    def selected(self, coordinate, grid):
        x = coordinate[0]
        y = coordinate[1]

        c = self.getXY()

        if x not in range (self.x, self.x + self.grid):
            return False

        if y not in range(self.y, self.y + self.grid):
            return False

        return True

    def getXY(self):

        x = (ord(self.coord[0]) - ord('A'))*self.grid + self.grid//2
        y = (8 - self.coord[1]) * self.grid + self.grid//2

        return [x,y]

    def updateCoord(self, coord):
        initialX = self.coord[0]
        initialY = self.coord[1]

        x = self.x + self.grid//2
        y = self.y + self.grid//2

        if coord != None:
            self.coord = coord
            return

        # ignore outside border
        y -= self.grid//2 
        x -= self.grid//2

        # reduce to 1,2,3 ...
        y = y//self.grid
        x = x//self.grid

        self.coord[0] = chr(ord('A') + x)
        self.coord[1] = 8 - y

        newXY = self.getXY()
        self.x = newXY[0]
        self.y = newXY[1]   

        # restrict to within the borders
        if self.x < self.grid//2:
            self.x += self.grid
        if self.x >= self.grid*8 + self.grid//2:
            self.x -= self.grid

        if self.y < self.grid//2:
            self.y += self.grid
        if self.y >= self.grid*8 + self.grid//2:
            self.y -= self.grid

        # if nothing changed return false
        if (initialX == self.coord[0] and initialY == self.coord[1]):
            return False
        return True


    def getName(self):
        string = 'models/'

        if self.colour == 'W':
            string += 'white'
        else:
            string += 'black'

        string += self.pieceType
        string += '.png'
        return string

    def draw(self, grid, window):
        # coord = self.getXY(grid)
        window.blit(self.image, (self.x,self.y, grid, grid))


class Game():
    def __init__(self, speed, grid):
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()
        self.clock = pygame.time.Clock()
        self.speed = speed
        self.grid = grid

    def resetGame(self):
        self.running = True
        self.turn = 'white'
        self.castle = [True, True]
        self.check = [False, False]


        self.whitePieces = self.initialPieces('W')
        self.blackPieces = self.initialPieces('B')

        self.boardState = []
        for _ in range(8):
            self.boardState.append([None]*8)

        for w in self.whitePieces:
            row = 8 - w.coord[1]
            col = ord(w.coord[0]) - ord('A') 
            self.boardState[row][col] = w

        for b in self.blackPieces:
            row = 8 - b.coord[1]
            col = ord(b.coord[0]) - ord('A') 
            self.boardState[row][col] = b

        for r in self.boardState:
            for q in r:
                if (q != None):
                    print (q.colour, q.pieceType, end =" ")
                else:
                    print(q, end = " ")
            print()

        self.window = pygame.display.set_mode((self.grid*8 + self.grid, self.grid*8 + self.grid))
        pygame.display.set_caption("Chess")

    def refresh(self):
        self.drawBoard()
        self.drawPieces()
        pygame.display.update()
        self.clock.tick(self.speed)


    def drawBoard(self):
        WHITE = (200,200,200)
        BROWN = (100,100,100)
        self.window.fill((255,255,255))
        pygame.draw.rect(self.window, WHITE, (self.grid//2, self.grid//2, self.grid*8, self.grid*8))


        font = pygame.font.SysFont('Comic Sans MS', self.grid//3)


        for col in range (8): # A,B,C along top and bottom
            text = font.render(chr(ord('A') + col), True, (0,0,0))
            self.window.blit(text,(self.grid - self.grid//20 + col*self.grid, self.grid//5))
            self.window.blit(text,(self.grid - self.grid//20 + col*self.grid, self.grid//5 + self.grid*8 + self.grid//2))

        for row in range(8): # 1,2,3 .. along left and right
            text = font.render(str(8 - row), True, (0,0,0))
            self.window.blit(text,(self.grid*8 + self.grid//5 + self.grid//2, self.grid*row + self.grid//3 + self.grid//2))
            self.window.blit(text,(self.grid//5, self.grid*row + self.grid//3 + self.grid//2))

        for row in range(8):
            isWhite = False
            if (row + 1)%2 == 0:
                isWhite = True

            for col in range(8):   
                if isWhite:
                    isWhite = False
                else:
                    isWhite = True

                if not isWhite: 
                    square = (col*self.grid + self.grid//2, row*self.grid + self.grid//2, self.grid, self.grid)
                    pygame.draw.rect(self.window, BROWN, square)

    def drawPieces(self):   
        for p in self.whitePieces:
            # coord = p.getXY(self.grid)
            # self.window.blit(self.draw(), (coord[0],coord[1], self.grid, self.grid))
            p.draw(self.grid, self.window)
        for p in self.blackPieces:
            # coord = p.getXY(self.grid)
            # self.window.blit(pygame.image.load(p.getName()), (coord[0],coord[1], self.grid, self.grid))
            p.draw(self.grid, self.window)


    # pygame.draw.rect(screen, RED, rectangle)
    def initialPieces(self, colour):
        result = []
        row = 2
        if (colour == 'B'):
            row = 7

        for n in range(8):
            result.append(Piece(self.grid, colour, 'Pawn', chr(ord('A') + n), row))

        row = 1
        if colour == 'B':
            row = 8

        result.append(Piece(self.grid, colour, 'Rook', 'A', row))
        result.append(Piece(self.grid, colour, 'Rook', 'H', row))

        result.append(Piece(self.grid, colour, 'Knight', 'B', row))
        result.append(Piece(self.grid, colour, 'Knight', 'G', row))

        result.append(Piece(self.grid, colour, 'Bishop','C', row))
        result.append(Piece(self.grid, colour, 'Bishop','F', row))

        result.append(Piece(self.grid, colour, 'King','E', row))
        result.append(Piece(self.grid, colour, 'Queen','D', row))

        return result
