import os
import math
import time
import pygame


class Game():

    def __init__(self, speed, width, height):
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()

        self.clock = pygame.time.Clock()
        self.speed = speed
        self.width = width
        self.height = height
        self.gravity = 2

        # colour defines
        self.RED = (255,0,0)
        self.GREEN = (0,255,0)
        self.BLUE = (0,0,255)
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)

    def resetGame(self):
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Swing!")

        self.running = True
        self.gameOver = False

        self.playerX = self.width//2     # player location
        # self.playerY = self.height//2
        self.playerY = 100
        
        self.velX = 0   # player direction
        self.velY = 0

        # initialise grapple
        self.pullTimer = 0
        self.pull = 0
        self.pullX = 0
        self.pullY = 0


    def refresh(self):
        self.clock.tick(self.speed) # game speed
        self.window.fill(self.WHITE)

        self.drawPlayer()
        self.drawBackground()

        pygame.display.update()

    def runGame(self):

        if (self.playerY in range(self.pullY - 10, self.pullY + 10) and \
            self.playerX in range(self.pullX - 10, self.pullX + 10)): # once we have reached our pull location
            
            self.pull = 0
            self.pullX = 0
            self.pullY = 0  
            self.pullTimer = 0
        self.velY += self.gravity # gravity

        if self.pull > 0: # we are grappling

            self.pullTimer -= 1

            xDist = self.playerX - self.pullX
            yDist = self.playerY - self.pullY

            if (xDist == 0):
                xDist = 1
            if (yDist == 0):
                yDist = 1

            xOffset = int(-1*xDist//(abs(xDist)**(0.75)))
            yOffset = int(-1*yDist//(abs(yDist)**(0.75)))
            self.velX += xOffset
            self.velY += yOffset


            # print(self.pullY)
            # print(self.pullX)

            # print()

            # self.pull = self.distance([self.pullX, self.pullY], [self.playerX, self.playerY])
            # self.pull -= int(((xOffset)**2 + (yOffset)**2)**(0.5))


        self.playerX += self.velX
        self.playerY += self.velY # move the player
            


        if (self.playerY >= self.height): # bounce off ground
            self.velY *= -1
            self.velY = self.velY*8//10
            self.playerY = self.height


        if (self.playerY <= 0):
            self.velY *= -1
            self.velY = self.velY*8//10
            self.playerY = 0      
        
        if (self.playerX >= self.width):
            self.velX *= -1
            self.velX = self.velX*8//10
            self.playerX = self.width

        if (self.playerX <= 0):
            self.velX *= -1
            self.velX = self.velX*8//10
            self.playerX = 0     



    def distance(self, point1, point2):
        return math.floor((abs(point1[0] - point2[0])**2 + abs(point1[1] - point2[1])**2)**(0.5))


    def drawPlayer(self):
        pygame.draw.circle(self.window, self.RED, (self.playerX, self.playerY), 10)
        if (self.pull > 0):
            pygame.draw.line(self.window, self.BLACK, \
                            (self.playerX, self.playerY), (self.pullX, self.pullY))


    def drawBackground(self):
        pass