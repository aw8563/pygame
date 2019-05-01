import math
import random
import pygame
import os
from abc import ABC, abstractmethod

screenHeight = 500
screenWidth = 250
grid = 25

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)
white = (255,255,255)

PIECETYPE = 99
class Piece():
    def __init__(self, pieceType):

        if pieceType == 1: # z1
            b3 = Block(100, 0, red)
            b2 = Block(125, 0, red)
            b1 = Block(125, 25, red)
            b4 = Block(150, 25, red)
            self.pivot = b1
        
        elif pieceType == 2: # z2
            b2 = Block(100, 25, (243,46,243))
            b1 = Block(125, 25, (243,46,243))
            b3 = Block(125, 0, (243,46,243))
            b4 = Block(150, 0, (243,46,243))
            self.pivot = b1
        
        elif pieceType == 3: # l1
            b3 = Block(100, 0, (238,255,10))
            b2 = Block(100, 25, (238,255,10))
            b1 = Block(100, 50, (238,255,10))
            b4 = Block(125, 50, (238,255,10))
            self.pivot = b1
        elif pieceType == 4: # l2
            b3 = Block(125, 0, (65,250,255))
            b2 = Block(125, 25,(65,250,255))
            b1 = Block(125, 50, (65,250,255))
            b4 = Block(100, 50, (65,250,255))
            self.pivot = b1
        
        elif pieceType == 5: # t
            b3 = Block(100, 25, (255,186,65))
            b2 = Block(125, 0, (255,186,65))
            b1 = Block(125, 25, (255,186,65))
            b4 = Block(150, 25, (255,186,65))
            self.pivot = b1
        elif pieceType == 6: # i
            b2 = Block(75, 0, (116,255,65))
            b3 = Block(100, 0, (116,255,65))
            b1 = Block(125, 0, (116,255,65))
            b4 = Block(150, 0, (116,255,65))
            self.pivot = b1
        else: 
            b1 = Block(100, 0, (127,109,111))
            b2 = Block(125, 0, (127,109,111))
            b3 = Block(100, 25, (127,109,111))
            b4 = Block(125, 25, (127,109,111))
            self.pivot = None
            pass

        self.body = [b1,b2,b3,b4]


    def move(self, direction, currentBlocks, alternate):
        if (direction == 'space'):
            depth = 0
            found = False
            while(not found):        
                for b in self.body:
                    if (b.y + depth*grid >= screenHeight or currentBlocks[(b.y + depth * grid)//grid][b.x//grid] != 0):
                        found = True
                        break

                if not found:
                    depth += 1

            for b in self.body:
                currentBlocks[(b.y + grid*(depth - 1))//grid][b.x//grid] = self.body[0].colour

            return False

        if (alternate):   
            for b in self.body:

                if b.checkFloor(currentBlocks):
                    # print(self.body[0].y,self.body[0].x)
                    for b in self.body:
                        currentBlocks[(b.y - grid)//grid][b.x//grid] = self.body[0].colour

                    return False

        if direction == 'up':
            self.rotate(currentBlocks)

        valid = True
        for b in self.body:
            valid = b.validMove(direction, currentBlocks)
            if valid == False:
                # b.move(None, currentBlocks)
                break

        if valid == True:
            for b in self.body:
                b.move(direction, currentBlocks)
        else:
            for b in self.body:
                b.move(None, currentBlocks)

        return True

    def drawPiece(self, window):

        for b in self.body:
            b.drawBlock(window)

    def rotate(self, currentBlocks):

        pivot = self.pivot
        if pivot == None:
            return False


        results = [0]*4
        for n in range(len(self.body)):
            b = self.body[n]
            if b != pivot:
                # same col
                if b.x == pivot.x:
                    diff = pivot.y - b.y

                    test = Block(b.x + diff, pivot.y, red)
                    results[n] = test

                    # b.x -= diff
                    # b.y = pivot.y

                # same row
                elif b.y == pivot.y:
                    diff = pivot.x - b.x

                    test = Block(pivot.x, pivot.y - diff, red)
                    results[n] = test

                    # b.x = pivot.x
                    # b.y += diff

                else: # diagonal
                    diffx = pivot.x - b.x
                    diffy = pivot.y - b.y

                    if diffx > 0 and diffy > 0:
                        test = Block(b.x + diffx*2, b.y, red)
                        results[n] = test

                    if diffx > 0 and diffy < 0:
                        test = Block(b.x, b.y - 2*diffx, red)
                        results[n] = test

                    if diffx < 0 and diffy < 0:
                        test = Block(b.x + diffx*2, b.y, red)
                        results[n] = test

                    if diffx < 0 and diffy > 0:
                        test = Block(b.x, b.y + 2*diffy, red)
                        results[n] = test

        valid = True
        for r in results:
            if (r != 0):
                valid = r.validMove(None,currentBlocks)
            if not valid:
                break

        if valid:
            for n in range(len(self.body)):
                if (n != 0):    
                    self.body[n].x = results[n].x
                    self.body[n].y = results[n].y

        return
class Block():
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.colour = colour


    def drawBlock(self, window):
        rectangle = (self.x + 2, self.y + 2, grid - 3, grid - 3)
        outline = (self.x, self.y, grid, grid)
        pygame.draw.rect(window, black, outline, 2)
        pygame.draw.rect(window, self.colour, rectangle)


    def checkFloor(self, currentBlocks):

        if self.y >= screenHeight:
            return True

        if currentBlocks[self.y//grid][self.x//grid] != 0:
            return True

        return False

    def validMove(self, direction, currentBlocks):
        x = self.x
        y = self.y

        if (direction == 'left'):
            x -= grid
        elif direction == 'right':
            x += grid

        if x < 0 or x >= screenWidth:
            return False

        if y >= screenHeight or y < 0:
            return False

        if currentBlocks[(y)//grid][x//grid] != 0:
            return False
            
        return True


    def move(self, direction, currentBlocks):
        if direction == 'left':
            self.x -= grid

        elif direction == 'right':
            self.x += grid

class Game():
    def __init__(self, gameSpeed):
        self.gameSpeed = gameSpeed
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()

    def clearLine(self):
        bottomLine = self.currentBlocks[-1]

        filled = True
        for b in bottomLine:
            if b != 1:
                filled = False
                break
        if filled:
            self.currentBlocks.pop()
            self.currentBlocks.insert(0,[0]*(screenWidth//grid))
            self.clear = True


    # def drawClearLine(self):
    #   rectangle = (screenHeight - grid, 0, screenWidth, grid)
    #   pygame.draw.rect(self.window, white, rectangle)


    def drawFloor(self):
        for row in range(len(self.currentBlocks)):
            for col in range(len(self.currentBlocks[row])):
                if self.currentBlocks[row][col] != 0:
                    rectangle = (col*grid + 2, row*grid + 2, grid - 3, grid - 3)
                    outline = (col*grid, row*grid, grid, grid)
                    pygame.draw.rect(self.window, black, outline, 2)
                    pygame.draw.rect(self.window, self.currentBlocks[row][col], rectangle)
                    



    def getDirection(self, alternate):
        result = None

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            result = 'left'
        if key[pygame.K_RIGHT]:
            result = 'right'
        if key[pygame.K_DOWN]:
            result = 'down'
            alternate = True
        if key[pygame.K_UP]:
            result = 'up'
        if key[pygame.K_SPACE]:
            result = 'space'
            return False, result

        if (alternate):
            for b in self.piece.body:
                b.y += grid

        return alternate, result
    def test(self):
        self.window.fill(white)
        self.piece.drawPiece(self.window)
        pygame.display.update()


    def refresh(self):
        if (self.gameOver):
            gOverFont = pygame.font.SysFont('Comic Sans MS', 50)
            gOver = gOverFont.render("GAME OVER", True, red)
            self.window.blit(gOver,(30,200))
            pygame.display.update()
            return
        if len(self.clearLines) > 0:
            for l in self.clearLines:
                pygame.draw.rect(self.window, white, (0, l*grid, screenWidth, grid))
            pygame.display.update()
            pygame.time.delay((100 - self.gameSpeed)//2)
            self.clearLines = []
        self.window.fill(white)
        self.piece.drawPiece(self.window)

        myfont = pygame.font.SysFont('Comic Sans MS', 25)
        score = myfont.render('Lines Cleared: ' + str(self.score), True, black)
        self.window.blit(score,(5, 10))

        self.drawFloor()

        # if (self.clear):
        #   self.clear = False
        #   print('here')
        #   self.drawClearLine()
        #   pygame.display.update()
        #   pygame.time.delay(100)

        pygame.display.update()
        pygame.time.delay(100 - self.gameSpeed)

    def resetGame(self):
        self.window = pygame.display.set_mode((screenWidth, screenHeight))
        self.gameOver = False
        arr = []
        for _ in range (screenHeight//grid):
            x = []
            for _ in range(screenWidth//grid):
                x.append(0)
            arr.append(x)

        # DEBUGGING

        # for n in range(10):
        #     if (n != 9):
        #         arr[19][n] = 1

        # for n in range(10):
        #     if (n != 9 and n != 8):
        #         arr[18][n] = 1

        # for n in range(10):
        #     if (n != 9):
        #         arr[17][n] = 1


        self.score = 0
        self.currentBlocks = arr

        # self.piece = Piece(random.randint(0,6))
        self.piece = Piece(6)

        self.running = True
        self.floor = [screenHeight]*(screenWidth//grid)
        self.clear = False
        self.hitFloor = False
        self.clearLines = []


    def runGame(self, alternate):
        if (self.gameOver):
            return
        alternate, direction = self.getDirection(alternate)
        self.hitFloor = (not self.piece.move(direction, self.currentBlocks, alternate))
        if self.hitFloor:
            for top in self.currentBlocks[0]:
                if top != 0:
                    self.gameOver = True
                    return
            self.piece = Piece(random.randint(0,6))


            # if (sum(self.currentBlocks[0]) > 0):
            #     self.gameOver = True
            #     return

            removal = []
            removal2 = []
            nRemoved = 0
            for line in range(len(self.currentBlocks)):
                # print(self.currentBlocks[line])

                full = True
                for n in self.currentBlocks[line]:
                    if n == 0:
                        full = False
                        break
                
                if full:
                        # print('here')
                        removal.append(line - nRemoved)
                        self.clearLines.append(line)
                        nRemoved += 1

            for n in removal:
                self.currentBlocks.pop(n)
            for _ in range(nRemoved):
                self.currentBlocks.insert(0,[0]*(screenWidth//grid))

            self.score += len(removal)

            






