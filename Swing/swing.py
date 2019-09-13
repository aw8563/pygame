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
        self.gravity = 10

        # colour defines
        self.RED = (255,0,0)
        self.GREEN = (0,255,0)
        self.BLUE = (0,0,255)
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)

    def resetGame(self):
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Swing!")
        print("=============================")
        self.debug = False
        self.running = True
        self.gameOver = False

        self.playerX = self.width//2 - 200     # player location
        # self.playerY = self.height//2
        self.playerY = 100
        
        self.velX = 0   # player direction
        self.velY = 0

        self.accelX = 0 # player momentum
        self.accelY = self.gravity

        # initialise grapple
        self.pull = 0
        self.pullX = 150
        self.pullY = 100
        self.angleVel = 0.1
        self.angelAccel = 0
        self.rotateDirection = 0
        # self.pull = self.distance([self.pullX, self.pullY], [self.playerX, self.playerY])
        # self.angle = math.atan(self.pullX - self.playerX/(self.pullY - self.playerY))


    def refresh(self):
        self.clock.tick(self.speed) # game speed
        self.window.fill(self.WHITE)
        self.draw()
        pygame.display.update()

    def runGame(self): # update game state 
        if self.pull > 0: # handle the 'swinging'
            self.arc() 
        else:
            # accelerate
            self.velY += self.accelY
            self.velX += self.accelX
            # update position
            self.playerY += self.velY
            self.playerX += self.velX


        self.bounce() # handle bouncing

    def arc(self):
        self.angleVel += self.angelAccel
        self.angle += self.rotateDirection*self.angleVel
        self.playerX = self.pullX + math.cos(self.angle)*self.pull
        self.playerY = self.pullY - math.sin(self.angle)*self.pull

        if (self.playerY <= self.pullY):
            print(self.velY)
            self.playerY += self.velY


    def bounce(self):
        # bounce off surface
        if (self.playerY >= self.height): # bounce off ground
            self.velY *= -1
            self.velY = self.velY*8//10
            self.playerY = self.height


        if (self.playerY <= 0): # top wall
            self.velY *= -1
            self.velY = self.velY*8//10
            self.playerY = 0      
        
        if (self.playerX >= self.width): # right wall
            self.velX *= -1
            self.velX = self.velX*8//10
            self.playerX = self.width

        if (self.playerX <= 0): # left wall
            self.velX *= -1
            self.velX = self.velX*8//10
            self.playerX = 0   

    def handleKeyPress(self, keys): # handle keys pressed

        if keys[pygame.K_q]: # quit game
            self.running = False

        if keys[pygame.K_r]: # restart game
            self.resetGame()

        if (keys[pygame.K_SPACE]):
            self.debug = True

        # no other keyboard commands

    def handleEvent(self, event): # handle mouse events

        if event.type == pygame.QUIT: # exit button
            self.running = False

        if event.type == pygame.MOUSEBUTTONDOWN: # on click
            # game.velY = 0

            self.pullX = event.pos[0]
            self.pullY = event.pos[1]
            # self.velX = 0
            # self.velY = 0
            self.pull = self.distance([self.pullX, self.pullY], [self.playerX, self.playerY])


            offsetX = self.playerX - self.pullX
            offsetY = -(self.playerY - self.pullY)

            if (offsetY == 0):
                if (offsetX > 0): # -->
                    self.angle = 0
                else: # <--
                    self.angle = math.pi

            self.angle = math.atan(offsetY/offsetX)

            if (offsetX > 0 and offsetY > 0): # first quadrant
                self.rotateDirection = -1
            elif (offsetX < 0 and offsetY > 0): # second quadrant
                self.angle += math.pi
                self.rotateDirection = 1
            elif (offsetX < 0 and offsetY < 0): # third quadrant
                self.angle += math.pi
                self.rotateDirection = 1
            else: # fourth quadrant
                self.angle += math.pi*2
                self.rotateDirection = -1

            self.angleVel = (self.velY/(2*math.pi*self.pull))*2*math.pi

        elif event.type == pygame.MOUSEBUTTONUP: # release click
            return
            self.pullX = 0
            self.pullY = 0
            self.pull = 0


    def draw(self):
        self.drawPlayer()
        self.drawBackground()
        # self.drawVelocity()
        # self.drawAcceleration()


    def drawPlayer(self):
        pygame.draw.circle(self.window, self.RED, (math.floor(self.playerX), math.floor(self.playerY)), 10)
        if (self.pull > 0): # draw the rope
            pygame.draw.line(self.window, self.BLACK, \
                            (int(self.playerX), int(self.playerY)), (int(self.pullX), int(self.pullY)))


    def drawVelocity(self):
        if (self.pull > 0):
            pygame.draw.line(self.window, self.BLUE, \
                            (self.playerX, self.playerY), (self.velX + self.playerX, self.velY + self.playerY))

    def drawAcceleration(self):
        if (self.pull > 0):
            pygame.draw.line(self.window, self.GREEN, \
                            (self.playerX, self.playerY), (self.playerX + self.accelX, self.playerY + self.accelY))

    def getAction(self):
        keys = pygame.key.get_pressed()            
        self.handleKeyPress(keys)


        for event in pygame.event.get():
            self.handleEvent(event)


    def drawBackground(self):
        pass

    def distance(self, point1, point2): # distance between point1 and point2
        return math.floor((abs(point1[0] - point2[0])**2 + abs(point1[1] - point2[1])**2)**(0.5))
