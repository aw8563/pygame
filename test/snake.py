import os
import math
import time
import pygame
import random


class Game():

    def __init__(self, speed, width, height):
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()

        self.clock = pygame.time.Clock()
        self.speed = speed
    
        self.grid = 10
        self.width = width*self.grid
        self.height = height*self.grid

        # colour defines
        self.RED = (255,0,0)
        self.GREEN = (0,255,0)
        self.BLUE = (0,0,255)
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)

    def resetGame(self):
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake")

        self.running = True
        self.gameOver = False

        self.snake = [[2*self.grid, 0*self.grid], [1*self.grid, 0*self.grid], [0*self.grid, 0*self.grid]]


        self.food = [random.randint(0, self.width//self.grid) * self.grid,
                     random.randint(0, self.height//self.grid) * self.grid]

        self.direction = 1 # up = 0, right = 1, down = 2, left = 3
        self.grow = False

    def refresh(self):
        self.clock.tick(self.speed) # game speed
        self.window.fill(self.WHITE)

        self.drawBackground()   
        self.drawSnake()
        self.drawFood()

        pygame.display.update()

    def runGame(self): # update game state 
        if not (self.grow):
            self.snake.pop() # remove tail if we are not growing
        else:
            self.grow = False

        newHead = self.snake[0].copy() # move head

        if self.direction == 0: # go up
            newHead[1] = self.snake[0][1] - self.grid
        elif self.direction == 1: # go right
            newHead[0] = self.snake[0][0] + self.grid
        elif self.direction == 2: # go down
            newHead[1] = self.snake[0][1] + self.grid
        else: # go left
            newHead[0] = self.snake[0][0] - self.grid

        # into wall
        if newHead[0] < 0 or newHead[0] > self.width - self.grid or \
           newHead[1] < 0 or newHead[1] > self.height - self.grid:

            self.gameOver = True
            self.running = False
           

        for body in self.snake: # run into itself
            if newHead[0] == body[0] and newHead[1] == body[1]:
                self.gameOver = True
                self.running = False
                break
        


        self.snake.insert(0, newHead)


        # food
        if newHead[0] == self.food[0] and newHead[1] == self.food[1]:
            self.grow = True 

            self.food = [random.randint(0, self.width//self.grid) * self.grid,
                         random.randint(0, self.height//self.grid) * self.grid]
    
    def handleKeyPress(self, keys): # handle keys pressed

        if keys[pygame.K_q]: # quit game
            self.running = False

        if keys[pygame.K_r]: # restart game
            self.resetGame()

        if keys[pygame.K_UP]:
            if (self.direction != 2):
                self.direction = 0

        if keys[pygame.K_RIGHT]:
            if (self.direction != 3):
                self.direction = 1

        if keys[pygame.K_DOWN]:
            if (self.direction != 0):
                self.direction = 2

        if keys[pygame.K_LEFT]:
            if (self.direction != 1):
                self.direction = 3

        # no other keyboard commands

    def doAction(self, action): # used for the ai
    
        if action == 0:
            if (self.direction != 2):
                self.direction = 0

        if action == 1:
            if (self.direction != 3):
                self.direction = 1

        if action == 2:
            if (self.direction != 0):
                self.direction = 2

        if action == 3:
            if (self.direction != 1):
                self.direction = 3


    def handleEvent(self, event): # handle mouse events

        if event.type == pygame.QUIT: # exit button
            self.running = False

    def drawSnake(self):


        for piece in self.snake:
            pygame.draw.rect(self.window, self.RED, (piece[0], piece[1], self.grid, self.grid))

    def drawFood(self):
        pygame.draw.rect(self.window, self.GREEN, (self.food[0], self.food[1], self.grid, self.grid))

    def getAction(self):
        for event in pygame.event.get():
            self.handleEvent(event)
        
        keys = pygame.key.get_pressed()            
        self.handleKeyPress(keys)

    def drawBackground(self):
        pass

