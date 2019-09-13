import numpy
import pygame
import math
import os
import time
import random

class Game():
    def __init__(self, width, height, speed = 1, grid = 5):

        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()

        self.clock = pygame.time.Clock()
        self.width = width
        self.height = height
        self.speed = speed
        self.grid = grid

        self.RED = (255,0,0)
        self.GREEN = (0,255,0)
        self.BLUE = (0,0,255)
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)



    def resetGame(self):
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("AI")

        self.running = True
        self.score = 0
        self.gameOver = False
        self.playerX = self.width//2 - self.grid*10
        self.playerY = self.height - self.grid*10
        self.resetEnemy()
        self.resetFood()
        self.vel = 10

    def refresh(self):
        # self.clock.tick()
        pygame.time.delay(30)
        self.window.fill(self.WHITE)

        self.draw()
        pygame.display.update()


    def draw(self):
        # draw the player
        pygame.draw.rect(self.window, self.BLUE, (self.playerX, self.playerY, self.grid*20, self.grid*3))

        # draw enemy
        # pygame.draw.rect(self.window, self.RED, (self.enemyX, self.enemyY, self.grid*5, self.grid*5))
        
        # draw food
        pygame.draw.rect(self.window, self.GREEN, (self.foodX, self.foodY, self.grid*5, self.grid*5))
        
        font = pygame.font.SysFont('Comic Sans MS', 25)
        scoreText = font.render("Score: " + str(self.score//100), True, self.BLACK)
        self.window.blit(scoreText, (25,25))
        pass


    def runGame(self):
        # pick up food
        if self.foodX in range(self.playerX - self.grid*5, self.playerX + self.grid*20) and \
           self.foodY in range(self.playerY - self.grid*5, self.playerY + self.grid*3):
            self.resetFood()
            self.score += 100


    def handleAction(self, action):
        if (action == 'QUIT'):
            self.running = False

        if action == 'RESTART':
            self.resetGame()


        # handle player movement
        if action == 0:
            self.playerX -= self.vel
            if self.playerX < 0:
                self.playerX = 0

        if action == 1:
            self.playerX += self.vel
            if self.playerX > self.width - self.grid*20:
                            self.playerX = self.width - self.grid*20

        # handle enemy movement (straight down)
        # self.enemyY += self.vel
        # if (self.enemyY > self.height):
        #     self.resetEnemy()

        # handles food (straihght down)
        self.foodY += self.vel
        if (self.foodY > self.height):
            # DIE!
            # self.score -= 10
            self.running = False
            self.resetFood()

    def handleEvent(self, event):
        if event.type == pygame.QUIT:
                self.running = False

    def resetEnemy(self):
        self.enemyX = random.randint(0,self.width//self.grid - 5)*self.grid
        self.enemyY = self.grid*5



    def resetFood(self):
        self.foodX = random.randint(0,self.width//self.grid - 5)*self.grid
        # self.foodX = 400
        self.foodY = self.grid*5


    def getObservation(self):
        inline = False
        if self.foodX in range(self.playerX - 5*self.grid, self.playerX + self.grid*20):
            inline = True

        return [self.playerX - self.foodX]