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
        self.wrongFlag = False
        self.boom = False

    def drawBlock(self, window, grid):
        BLACK = (0,0,0)
        GRAY = (150,150,150)
        RED = (255,0,0)

        outlineRectangle = (self.col*grid, self.row*grid, grid, grid)
        rectangle = (self.col*grid + 1, self.row*grid + 1, grid - 1.4, grid - 1.4)
        circle = (self.col*grid + grid//2, self.row*grid + grid//2)


        pygame.draw.rect(window, BLACK, outlineRectangle)
        
        if (self.revealed):
            pygame.draw.rect(window, (100,100,100), rectangle)

            if (not self.mine and self.nAdjacent > 0):
                font = pygame.font.SysFont('Comic Sans MS', grid + grid//2)
                text = font.render(str(self.nAdjacent), True, (0,0,0))
                window.blit(text,(self.col*grid + grid//4, self.row*grid + grid//10))

            elif self.mine:
                if (self.boom):
                    GRAY = (255,0,0)
                pygame.draw.rect(window, GRAY, rectangle)
                pygame.draw.circle(window, BLACK, circle, grid//4)

        else:
            rectangle = (self.col*grid + 1, self.row*grid + 1, grid - 1.4, grid - 1.4)
            pygame.draw.rect(window, GRAY, rectangle)
            if (self.flagged):
                pygame.draw.circle(window, RED, circle, grid//4)    
                if self.wrongFlag:
                    line1Start = (self.col*grid, self.row*grid)
                    line1End = (self.col*grid + grid, self.row*grid + grid)

                    line2Start = (self.col*grid + grid, self.row*grid)
                    line2End = (self.col*grid, self.row*grid + grid)     

                    pygame.draw.line(window, RED, line1Start, line1End)
                    pygame.draw.line(window, RED, line2Start, line2End)

class Game():
    def __init__(self, speed, width, height, nMines):
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()
        self.clock = pygame.time.Clock()
        self.speed = speed
        self.grid = 20
        self.width = width
        self.height = height
        self.screenWidth = width * self.grid
        self.screenHeight = (height + 1)* self.grid
        self.nMines = nMines

    def showBoard(self):
        for line in self.boardState:
            for cell in line:
                print(cell.nAdjacent, end = " ")
            print()

    def addMines(self, startRow, startCol): # add mines to all cells except x and y
        for _ in range(self.nMines):
            
            row = random.randint(0,self.height - 1)
            col = random.randint(0,self.width - 1)

            # makes sure there aren't overlaps
            while (self.boardState[row][col].mine or (row == startRow and col == startCol)):
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
   


    def resetGame(self):
        self.win = False
        self.running = True
        self.firstMove = True
        self.gameOver = False
        self.window = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption("Minesweeper")

        # create initial board
        board = []
        for row in range(self.height):
            l = []
            for col in range(self.width):
                l.append(Block(row, col, False))
            board.append(l)

        self.boardState = board
        self.nMinesRemaining = self.nMines
        self.nRevealed = 0

    def refresh(self):
        self.clock.tick(self.speed)
        self.window.fill((0,0,0))
        self.drawBoard()

        if (self.gameOver or self.win):
            for row in self.boardState:
                for block in row:
                    if (block.mine):
                        block.revealed = True
                        block.drawBlock(self.window, self.grid)

        pygame.display.update()

    def drawBoard(self):

        for row in self.boardState:
            for block in row:
                block.drawBlock(self.window, self.grid)


        rectangle = (0,self.grid*self.height, self.grid*self.width, self.grid)
        if self.gameOver:
            pygame.draw.rect(self.window, (255,0,0), rectangle)

        # if self.nRevealed == (self.width * self.height - self.nMines):
        if self.win:
            pygame.draw.rect(self.window, (0,255,0), rectangle)


        font = pygame.font.SysFont('Comic Sans MS', self.grid + self.grid//5)
        text = font.render("Mines Left " + str(self.nMinesRemaining), True, (255,255,255))
        self.window.blit(text, (self.grid*self.width//2 - self.grid*2.5, (self.height)*self.grid + self.grid//10))
        # self.window.blit(text, 50,50)
    def updateBoard(self, x, y, action):
        row = y//self.grid
        col = x//self.grid

        if action == 'flag' and not self.boardState[row][col].revealed: 

            cell = self.boardState[row][col]

            if (cell.flagged):
                cell.flagged = False
                self.boardState[row][col].wrongFlag = False
                self.nMinesRemaining += 1

            else:
                cell.flagged = True
                self.nMinesRemaining -= 1

        elif action == 'reveal' and not self.boardState[row][col].flagged:
            if self.firstMove:
                self.addMines(row,col)# add mines
                self.firstMove = False

            if (self.boardState[row][col].mine):
                self.boardState[row][col].boom = True
                self.gameOver = True
                print("You lost!")
                return
            self.revealBlank(row, col)

        elif action == 'force' and self.boardState[row][col].revealed:
            nFlagsAdjacent = 0

            checks = [(1,0), (0,1), (-1,0), (0,-1), (1,1), (-1,1), (-1,-1), (1,-1)]
            lose = False
            wrongFlags = []
            for c in checks:
                newRow = row + c[0]
                newCol = col + c[1]

                if (newRow < self.height and newRow >= 0 and newCol < self.width and newCol >= 0):
                    if (self.boardState[newRow][newCol].flagged):
                        nFlagsAdjacent += 1
                        if not (self.boardState[newRow][newCol].mine):
                            wrongFlags.append((newRow, newCol))
                            lose = True


            if nFlagsAdjacent >= self.boardState[row][col].nAdjacent:
                if (lose):
                    for pair in wrongFlags:
                        self.boardState[pair[0]][pair[1]].wrongFlag = True
                    self.gameOver = True
                    print("You lost!")
                    return
                for c in checks:
                    newRow = row + c[0]
                    newCol = col + c[1]                    
                    if (newRow < self.height and newRow >= 0 and newCol < self.width and newCol >= 0):
                        if not (self.boardState[newRow][newCol].flagged):
                            self.revealBlank(newRow, newCol)                    



    def revealBlank(self, row, col):
        if self.boardState[row][col].revealed or self.boardState[row][col].flagged:
            return
        if self.boardState[row][col].mine:
            self.gameOver = True
            print("You lost!")
            return
        self.boardState[row][col].revealed = True
        self.nRevealed += 1
        if self.boardState[row][col].nAdjacent != 0:
            return

        checks = [(1,0), (0,1), (-1,0), (0,-1), (1,1), (-1,1), (-1,-1), (1,-1)]
        for c in checks:
            newRow = row + c[0]
            newCol = col + c[1]

            if (newRow < self.height and newRow >= 0 and newCol < self.width and newCol >= 0):
                self.revealBlank(newRow, newCol)


    def runGame(self, event):
        if self.gameOver:
            return 

        if self.nRevealed == (self.width * self.height - self.nMines):
            self.nMinesRemaining = 0
            self.win = True
            self.nRevealed = 0
            print("You won!")
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            x = event.pos[0]
            y = event.pos[1]
            mousePressed = pygame.mouse.get_pressed()
            if mousePressed[0] and mousePressed[2]:
                self.updateBoard(x,y, 'force')
                return
            if event.button == 1: # left click
                self.updateBoard(x,y, 'reveal')
            elif event.button == 3: # right click (flag)
                self.updateBoard(x,y, 'flag')   

