import pygame 
import os
import math
import random
import time
from Pieces import *

class Game():
    def __init__(self, grid):
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()
        self.clock = pygame.time.Clock()
        self.speed = 30
        self.grid = grid
        self.window = pygame.display.set_mode((self.grid*8 + self.grid, self.grid*10 + self.grid))
        self.mode = "home"
        pygame.display.set_caption("Chess")


    def resetGame(self):
        self.turn = 'W'
        self.running = True
        self.board = []
        self.movingPiece = None
        self.whiteKing = None
        self.blackKing = None
        self.whiteTimer = None
        self.blackTimer = None
        self.whiteRemaining = 100
        self.blackRemaining = 100


        for _ in range(8):
            row = [None]*8
            self.board.append(row)



        self.resetBoard()

    def showBoard(self):
        for r in self.board:
            for c in r:
                print(c, end = " ")
            print()



    def refresh(self):
        self.window.fill((150, 148, 138))
        if (self.mode == "home"):
            self.drawHome()

        elif self.mode == "1p" or self.mode == "2p":

            whiteTime = self.whiteRemaining
            blackTime = self.blackRemaining

            if self.turn == "W" and self.whiteTimer:
                # tick white timer
                whiteTime = self.whiteRemaining - ((pygame.time.get_ticks() - self.whiteTimer)/1000)
                    
            elif self.turn == "B" and self.blackTimer:
                # tick white timer
                blackTime = self.blackRemaining - ((pygame.time.get_ticks() - self.blackTimer)/1000)
                            



            self.drawHomeButton()
            self.drawBoard()
            self.drawIndicator()
            self.drawPieces()
            self.drawTimers(whiteTime, blackTime)
            # self.showTurn()
        pygame.display.update()

    def drawTimers(self,whiteTime, blackTime):
        font = pygame.font.Font(None, 40)

        if (self.turn == "W"):
            time1 = font.render(str(int(whiteTime)), True, (255,0,0))
            time2 = font.render(str(int(blackTime)), True, (0,0,0))
            outline = (self.grid + self.grid//2, self.grid*9 + self.grid//2, self.grid*2, self.grid)    

        else:
            time1 = font.render(str(int(whiteTime)), True, (0,0,0))
            time2 = font.render(str(int(blackTime)), True, (255,0,0))
            outline = (self.grid*5 + self.grid//2, self.grid*9 + self.grid//2, self.grid*2, self.grid)    

        pygame.draw.rect(self.window, (255, 0, 0), outline, 3)
        pygame.draw.rect(self.window, (200,200,200), (self.grid + self.grid//2, self.grid*9 + self.grid//2,\
                                                      self.grid*2, self.grid))

        pygame.draw.rect(self.window, (100,100,100), (self.grid*5 + self.grid//2, self.grid*9 + self.grid//2,\
                                                      self.grid*2, self.grid))

        # self.window.blit(text1, (self.grid*3 + (self.grid*3 - text1.get_rect().width)//2, \
        #                          self.grid*2 + (self.grid - text1.get_rect().height)//2))

        rectangle1 = ((self.grid + self.grid//2 + (self.grid*2 - time1.get_rect().width)//2,\
                    self.grid*9 + self.grid//2 + (self.grid - time1.get_rect().height)//2))

        rectangle2 = ((self.grid*5 + self.grid//2 + (self.grid*2 - time1.get_rect().width)//2,\
                    self.grid*9 + self.grid//2 + (self.grid - time1.get_rect().height)//2))


        self.window.blit(time1, rectangle1)
        self.window.blit(time2, rectangle2)

    def drawHomeButton(self):
        font = pygame.font.Font(None, 20)
        text = font.render("BACK", True, (0,0,0))

        self.window.blit(text,(2,4))

    def drawIndicator(self):
        if self.movingPiece != None:

            for move in self.movingPiece.moves:
                x = move[1]*self.grid + self.grid//2
                y = move[0]*self.grid + self.grid//2
                if self.turn == "B":
                    y = self.grid*8 - y

                indicator = pygame.Surface((self.grid, self.grid))
                indicator.set_alpha(64)
                indicator.fill((0,255,0)) 
                self.window.blit(indicator, (x,y))

    def showTurn(self):
        shift = 0
        if (self.turn == 'W'):
            shift = 8           
        pygame.draw.rect(self.window, (0,0,0), (self.grid*9-self.grid//2, self.grid//4 + shift*self.grid + \
                                                shift/8*self.grid//4, self.grid//4, self.grid//4))        

    def drawHome(self):

        colour = (232, 182, 32)
        pygame.draw.rect(self.window, colour, (self.grid*3, self.grid*2, self.grid*3, self.grid))
        pygame.draw.rect(self.window, colour, (self.grid*3, self.grid*4, self.grid*3, self.grid))
        pygame.draw.rect(self.window, colour, (self.grid*3, self.grid*6, self.grid*3, self.grid))

        font = pygame.font.Font(None, 35)
        text1 = font.render("Vs Computer", True, (0,0,0))
        text2 = font.render("Vs Human", True, (0,0,0))
        text3 = font.render("Custom", True, (0,0,0))


        self.window.blit(text1, (self.grid*3 + (self.grid*3 - text1.get_rect().width)//2, \
                                 self.grid*2 + (self.grid - text1.get_rect().height)//2))

        self.window.blit(text2, (self.grid*3 + (self.grid*3 - text2.get_rect().width)//2, \
                                 self.grid*4 + (self.grid - text2.get_rect().height)//2))

        self.window.blit(text3, (self.grid*3 + (self.grid*3 - text3.get_rect().width)//2, \
                                 self.grid*6 + (self.grid - text3.get_rect().height)//2))
        

    def drawPieces(self):
       


        for row in self.board:
            for piece in row:
                if piece != None:
                    piece.draw(self.grid, self.window, self.turn)

        if self.movingPiece != None:
            self.movingPiece.draw(self.grid, self.window, self.turn)

    def drawBoard(self):
        WHITE = (235, 203, 134)
        BROWN = (156, 108, 5)
        # self.window.fill((255,255,255))

        pygame.draw.rect(self.window, WHITE, (self.grid//2, self.grid//2, self.grid*8, self.grid*8))


        font = pygame.font.SysFont('Comic Sans MS', self.grid//3)


        for col in range (8): # A,B,C along top and bottom
            text = font.render(chr(ord('A') + col), True, (0,0,0))
            self.window.blit(text,(self.grid - self.grid//20 + col*self.grid, self.grid//5))
            self.window.blit(text,(self.grid - self.grid//20 + col*self.grid, self.grid//5 + self.grid*8 + self.grid//2))

        for row in range(8): # 1,2,3 .. along left and right
            text = font.render(str(8 - row), True, (0,0,0))
            if self.turn == "B":
                row = 7 - row
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


    def handleAction(action):
        pass

    def move(self, row, col, newRow, newCol):

        piece = self.board[row][col]
        if piece == None:

            return False
            
        if ((newRow, newCol) in piece.moves):

            self.updateEnPassant()
            piece.moveTo(newRow, newCol)




            blackMove = False   
            whiteMove = False

            for row in self.board:
                for p in row:
                    if (p == None):
                        continue

                    king = self.whiteKing if self.turn == "B" else self.blackKing
                    p.moves = p.getMoves(king)

                    if p.colour == "W" and len(p.moves) > 0:
                        whiteMove = True # possible moves for white
            
                    elif p.colour == "B" and len(p.moves) > 0:
                        blackMove = True # possible moves for black


            if not (blackMove or whiteMove):
                winner = "WHITE " if whiteMove else "BLACK "
                winner += "WINS!"
                print(winner)
                self.running = False
                return

            if (self.turn == "W"):
                self.turn = "B"
                self.blackTimer = pygame.time.get_ticks()
                if self.whiteTimer:
                    time = ((pygame.time.get_ticks() - self.whiteTimer)/1000)
                    self.whiteRemaining -= time
            else:
                self.turn = "W"
                self.whiteTimer = pygame.time.get_ticks()

                if self.blackTimer:
                    time = ((pygame.time.get_ticks() - self.blackTimer)/1000)
                    self.blackRemaining -= time
            return True

        else:
            return False

    def resetBoard(self):
        for i in range(8):
            self.board[1][i] = Pawn(self.board, 1, i, 'B')
            self.board[6][i] = Pawn(self.board, 6, i, 'W')

        self.board[0][0] = Rook(self.board, 0, 0, 'B')
        self.board[0][7] = Rook(self.board, 0, 7, 'B')
        self.board[7][0] = Rook(self.board, 7, 0, 'W')
        self.board[7][7] = Rook(self.board, 7, 7, 'W')

        self.board[0][1] = Knight(self.board, 0, 1, 'B')
        self.board[0][6] = Knight(self.board, 0, 6, 'B')
        self.board[7][1] = Knight(self.board, 7, 1, 'W')
        self.board[7][6] = Knight(self.board, 7, 6, 'W')
        
        self.board[0][2] = Bishop(self.board, 0, 2, 'B')
        self.board[0][5] = Bishop(self.board, 0, 5, 'B')
        self.board[7][2] = Bishop(self.board, 7, 2, 'W')
        self.board[7][5] = Bishop(self.board, 7, 5, 'W')

        self.board[0][3] = Queen(self.board, 0, 3, 'B')
        self.board[7][3] = Queen(self.board, 7, 3, 'W')

        self.board[0][4] = King(self.board, 0, 4, 'B')
        self.board[7][4] = King(self.board, 7, 4, 'W')

        self.whiteKing = self.board[7][4]
        self.blackKing = self.board[0][4]


        for row in self.board:
            for piece in row:
                if piece != None:
                    piece.moves = piece.getMoves(self.whiteKing)

    def updateEnPassant(self):
        for i in range(8):
            p = self.board[3][i]
            if p != None and isinstance(p, Pawn):
                p.enPassant = False
            p = self.board[4][i]
            if p != None and isinstance(p, Pawn):
                p.enPassant = False

    def computerMove(self): # random for now
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != None and piece.colour == self.turn and len(piece.moves) > 0:
                    pieces.append(piece)

        if len(pieces) == 0:
            print("YOU WIN!")
            self.running = False
            return
        pieceToMove = pieces[random.randint(0, len(pieces) - 1)]
        move = pieceToMove.moves[random.randint(0, len(pieceToMove.moves) - 1)]

        self.move(pieceToMove.row, pieceToMove.col, move[0], move[1])

if __name__ == '__main__':
    print("helloworld!")
    game = Game(50)
    game.resetGame()

    game.showBoard()

    print(game.board[1][0].getMoves(1,0))


