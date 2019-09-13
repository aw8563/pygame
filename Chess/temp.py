import pygame
import os
import math
import time
from abc import ABC, abstractmethod
from Pieces import *

WHITE = (200,200,200)
BROWN = (100,100,100)

class Game():
    def __init__(self, speed, grid):
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()
        self.clock = pygame.time.Clock()
        self.speed = 30
        self.grid = grid

    # returns true/false if the king is in check

    def resetGame(self):
        self.playingPiece = None
        self.running = True
        self.turn = 'white'
        self.blackCastle = [True, True]
        self.whiteCastle = [True, True]

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


        self.whiteKing = self.boardState[7][4]
        self.blackKing = self.boardState[0][4]
        self.window = pygame.display.set_mode((self.grid*8 + self.grid, self.grid*8 + self.grid))
        pygame.display.set_caption("Chess")

    def refresh(self):
        self.drawBoard()
        self.drawPieces()
        self.drawIndicator()
        pygame.display.update()
        self.clock.tick(self.speed)

    def drawIndicator(self):
        shift = 0
        if (self.turn == 'white'):
            shift = 8           
        pygame.draw.rect(self.window, (0,0,0), (self.grid//4, self.grid//4 + shift*self.grid + shift/8*self.grid//4,\
                         self.grid//4, self.grid//4))



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
        for row in self.boardState:
            for col in row:
                if col != None:
                    col.draw(self.grid, self.window)

        if self.playingPiece != None:
            self.playingPiece.draw(self.grid, self.window)      
                
    # pygame.draw.rect(screen, RED, rectangle)
    def initialPieces(self, colour):
        result = []
        row = 2
        if (colour == 'B'):
            row = 7

        for n in range(8):
            result.append(Pawn(self.grid, colour, 'Pawn', chr(ord('A') + n), row))

        row = 1
        if colour == 'B':
            row = 8

        result.append(Rook(self.grid, colour,'Rook', 'A', row))
        result.append(Rook(self.grid, colour,'Rook','H', row))

        result.append(Knight(self.grid, colour,'Knight', 'B', row))
        result.append(Knight(self.grid, colour,'Knight', 'G', row))

        result.append(Bishop(self.grid, colour,'Bishop', 'C', row))
        result.append(Bishop(self.grid, colour, 'Bishop','F', row))

        result.append(King(self.grid, colour,'King', 'E', row))
        result.append(Queen(self.grid, colour,'Queen', 'D', row))

        return result


    def updateCoord(self):
        piece = self.playingPiece
        initialX = piece.coord[0]
        initialY = piece.coord[1]
        board = self.boardState

        # restrict to within the borders
        if piece.x < 0:
            piece.x += piece.grid
        if piece.x >= piece.grid*8 + piece.grid//2:
            piece.x -= piece.grid

        if piece.y < 0:
            piece.y += piece.grid
        if piece.y >= piece.grid*8 + piece.grid//2:
            piece.y -= piece.grid


        x = piece.x + piece.grid//2
        y = piece.y + piece.grid//2

        # ignore outside border
        y -= piece.grid//2 
        x -= piece.grid//2

        # reduce to 1,2,3 ...
        y = y//piece.grid
        x = x//piece.grid

        newX = chr(ord('A') + x) # A
        newY = 8 - y # 1,2,3

        print(piece.colour, piece.pieceType, piece.coord[0], piece.coord[1],'-->', newX, newY, end = " ")

        valid = piece.isValidMove(board, newX, newY)
        if not valid:
            print('FAILED invalid move')
            return False
        
        piece.coord[0] = newX
        piece.coord[1] = newY

        newXY = piece.getXY()
        piece.x = newXY[0]
        piece.y = newXY[1]   


        # if nothing changed return false
        if (initialX == piece.coord[0] and initialY == piece.coord[1]):
            print("SAME SPOT")
            for b in board:
                print(b)
            return False

        # update the board here
        old = board[8 - newY][ord(newX) - ord('A')]
        board[8 - newY][ord(newX) - ord('A')] = piece



        if (old != None):
            print(" (takes)", old.colour, old.pieceType)
        else:
            print()

        board[8 - initialY][ord(initialX) - ord('A')] = None

        # make sure king is not in check
        if (self.inCheck()):
            board[8 - newY][ord(newX) - ord('A')] = old
            board[8 - initialY][ord(initialX) - ord('A')] = piece
            piece.coord = [initialX, initialY]


            print("FAILED. in check")                                 
            return False

        else: # not in check
            if board[0][0] == None:
                self.blackCastle[1] = False
            if board[0][7] == None:
                self.blackCastle[0] = False

            if board[7][0] == None:
                self.whiteCastle[1] = False
            if board[7][7] == None:
                self.whiteCastle[0] = False
            
            # update castling
            success = False or not (valid == 'kingCastle' or valid == 'queenCastle')
            if valid == 'kingCastle' and False:

                if self.blackCastle[0] and piece.colour == 'B' and board[0][7].colour == 'B' and \
                   board[0][7].pieceType == 'Rook': #and self.blackCastle[0]:
                    rook = board[0][7]
                    board[0][5] = rook
                    board[0][7] = None
                    rook.coord = ['F', 8]
                    xy = rook.getXY()
                    rook.x = xy[0]
                    rook.y = xy[1]
                    self.blackCastle = [False, False]
                    success = True

                elif self.whiteCastle[0] and piece.colour == 'W' and board[7][7].colour == 'W' and \
                     board[7][7].pieceType == 'Rook': # and self.whiteCastle[0]:

                    rook = board[7][7]
                    board[7][5] = rook
                    board[7][7] = None
                    rook.coord = ['F', 1]
                    xy = rook.getXY()
                    rook.x = xy[0]
                    rook.y = xy[1]
                    success = True
                    self.whiteCastle = [False, False]

            elif valid == 'queenCastle':
                if self.blackCastle[1] and piece.colour == 'B' and board[0][0].colour == 'B' and \
                   board[0][0].pieceType == 'Rook': #and self.blackCastle[1]:
                    row = 7
                    rook = board[0][0]
                    board[0][3] = rook
                    board[0][0] = None
                    rook.coord = ['D', 8]
                    xy = rook.getXY()
                    rook.x = xy[0]
                    rook.y = xy[1]
                    success = True
                    self.blackCastle = [False, False]

                elif self.whiteCastle[1] and piece.colour == 'W' and board[7][0].colour == 'W' and \
                     board[7][0].pieceType == 'Rook':

                    rook = board[7][0]
                    board[7][3] = rook
                    board[7][0] = None
                    rook.coord = ['D', 1]
                    xy = rook.getXY()
                    rook.x = xy[0]
                    rook.y = xy[1]
                    success = True
                    self.whiteCastle = [False, False]

            if (not success):
                print('here')
                board[8 - newY][ord(newX) - ord('A')] = None
                board[8 - initialY][ord(initialX) - ord('A')] = piece
                piece.coord = [initialX, initialY]
                print(initialX, initialY)
                return False
                
            print('white', self.whiteCastle)
            print('black', self.blackCastle)
        

        return True

    def inCheck(self):
        board = self.boardState
        turn = self.turn
        king = self.whiteKing

        if self.turn == 'black':
            king = self.blackKing

        coord = [0,0]
        coord[1] = ord(king.coord[0]) - ord('A')
        coord[0] = 8 - king.coord[1]


        # check diagonals
        row = coord[0] - 1
        col = coord[1] + 1
        while (row >= 0 and col < 8):

            if (board[row][col] != None):    
                piece = board[row][col]
                if piece.colour != king.colour: # enemy piece
                    # check if it is a bishop or queen
                    if piece.pieceType == "Queen" or piece.pieceType == "Bishop":
                        return True
                    else:
                        break
                else: # same piece
                    break
            row -= 1
            col += 1
        

        row = coord[0] + 1
        col = coord[1] + 1
        while (row < 8 and col < 8):

            if (board[row][col] != None):    
                piece = board[row][col]
                if piece.colour != king.colour: # enemy piece
                    # check if it is a bishop or queen
                    if piece.pieceType == "Queen" or piece.pieceType == "Bishop":
                        return True
                    else:
                        break
                else: # same piece
                    break
            row += 1
            col += 1


        row = coord[0] - 1
        col = coord[1] - 1
        while (row >= 0 and col >= 0):

            if (board[row][col] != None):    
                piece = board[row][col]
                if piece.colour != king.colour: # enemy piece
                    # check if it is a bishop or queen
                    if piece.pieceType == "Queen" or piece.pieceType == "Bishop":
                        return True
                    else:
                        break
                else: # same piece
                    break
            row -= 1
            col -= 1


        row = coord[0] + 1
        col = coord[1] - 1
        while (row < 8 and col >= 0):

            if (board[row][col] != None):    
                piece = board[row][col]
                if piece.colour != king.colour: # enemy piece
                    # check if it is a bishop or queen
                    if piece.pieceType == "Queen" or piece.pieceType == "Bishop":
                        return True
                    else:
                        break
                else: # same piece
                    break
            row += 1
            col -= 1

        # check vertical/horizontal lines

        row = coord[0] + 1
        col = coord[1]
        while (row < 8):

            if (board[row][col] != None):    
                piece = board[row][col]
                if piece.colour != king.colour: # enemy piece
                    # check if it is a rook or queen
                    if piece.pieceType == "Queen" or piece.pieceType == "Rook":
                        return True
                    else:
                        break
                else: # same piece
                    break
            row += 1

        row = coord[0] - 1
        col = coord[1]
        while (row >= 0):

            if (board[row][col] != None):    
                piece = board[row][col]
                if piece.colour != king.colour: # enemy piece
                    # check if it is a rook or queen
                    if piece.pieceType == "Queen" or piece.pieceType == "Rook":
                        return True
                    else:
                        break
                else: # same piece
                    break
            row -= 1

        row = coord[0]
        col = coord[1] + 1
        while (col < 8):

            if (board[row][col] != None):    
                piece = board[row][col]
                if piece.colour != king.colour: # enemy piece
                    # check if it is a rook or queen
                    if piece.pieceType == "Queen" or piece.pieceType == "Rook":
                        return True
                    else:
                        break
                else: # same piece
                    break
            col += 1

        row = coord[0] 
        col = coord[1] - 1
        while (col >= 0):

            if (board[row][col] != None):    
                piece = board[row][col]
                if piece.colour != king.colour: # enemy piece
                    # check if it is a rook or queen
                    if piece.pieceType == "Queen" or piece.pieceType == "Rook":
                        return True
                    else:
                        break
                else: # same piece
                    break
            col -= 1
        
        # check for knight checks

        moves = [[1,2], [1,-2], [2,1], [2,-1], [-1,-2], [-2,-1], [-1,2], [-2,1]]
        for pair in moves:
            row = coord[0] + pair[0]
            col = coord[1] + pair[1]

            if (row >= 0 and col >= 0 and row < 8 and col < 8):
                # print(row,col, board[row][col])

                if (board[row][col] != None):
                    if (board[row][col].colour != king.colour and board[row][col].pieceType == "Knight"):
                        return True

        # check for king checks

        moves = [[1,0], [1,1], [0,1], [0,-1], [-1,0], [-1,-1], [-1,1], [1,-1]]
        for pair in moves:
            row = coord[0] + pair[0]
            col = coord[1] + pair[1]

            if (row >= 0 and col >= 0 and row < 8 and col < 8):
                if (board[row][col] != None):
                    if (board[row][col].colour != king.colour and board[row][col].pieceType == "King"):
                        return True

        # check for pawn checks
        moves = [[-1,1], [-1,-1]] #white

        if king.colour == 'B': #black
            moves = [[1,1],[1,-1]]
        
        for pair in moves:
            row = coord[0] + pair[0]
            col = coord[1] + pair[1]

            if (row >= 0 and col >= 0 and row < 8 and col < 8):
                if (board[row][col] != None):
                    if (board[row][col].colour != king.colour and board[row][col].pieceType == "Pawn"):
                        return True 
                
        return False
