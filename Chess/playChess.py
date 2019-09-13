from chess import *
import os
import pygame
import math
import time



grid = 60
game = Game(grid)
game.resetGame()



row = 0
col = 0
piece = None
offset_x = 0
offset_y = 0



def main():

    moving = False
    while(game.running):

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_q]):
            game.running = False

        if (keys[pygame.K_r]):
            game.resetGame()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False


            if game.mode == "home":
                homeAction(event)
            elif game.mode == "1p":
                gameAction(event, True) # single player
            elif game.mode == "2p":
                gameAction(event, False)
            elif game.mode == "computer":
                pass

        game.refresh()

    print("DONE!")

def gameAction(event, computer):

    if event.type == pygame.MOUSEBUTTONDOWN:
        global row, col, piece, offset_x, offset_y
        

        if event.button == 1:
            
            # get piece here
            
            clickX = event.pos[0]
            clickY = event.pos[1]   

            if clickX in range(37) and clickY in range(14):
                game.resetGame()
                game.mode = "home"
                return


            if (game.turn == "B"):
                clickY = grid*9 - clickY

            clickX += grid//2
            clickY += grid//2

            clickY //= grid
            clickX //= grid           

            row = clickY - 1
            col = clickX - 1

            piece = None
            if (row >= 0 and row < 8 and col >= 0 and col < 8):
                piece = game.board[row][col]

            if piece != None and piece.colour == game.turn:
                moving = True
                game.movingPiece = piece
                mouse_x, mouse_y = event.pos
                

                offset_x = piece.x - mouse_x
                offset_y = piece.y - mouse_y

                if (game.turn == 'B'):
                    offset_y = grid*9 - piece.y - mouse_y

    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:            
            
            if (game.movingPiece != None):
                newRow, newCol = piece.fit()
                
                # check the move is valid   

                if (game.move(row, col, newRow, newCol)):
                    if computer:
                        game.computerMove()
                else:
                    piece.reset()

        game.movingPiece = None
        moving = False
            

    elif event.type == pygame.MOUSEMOTION:
        if game.movingPiece != None:
            mouse_x, mouse_y = event.pos


            piece.x = mouse_x + offset_x
            piece.y = mouse_y + offset_y
            if (game.turn == 'B'):
                piece.y = grid*9 - piece.y


def homeAction(event):
    # 193, 137
    if event.type == pygame.MOUSEBUTTONDOWN:

        if event.button == 1: # left click only
            x,y = event.pos[0], event.pos[1]

            if x in range(grid*3, grid*6):
                if y in range(grid*2, grid*3):
                    print("1p")
                    game.mode = "1p"

                elif y in range(grid*4, grid*5):
                    print('2p')
                    game.mode = "2p"

                elif y in range(grid*6, grid*7):
                    print('custom')
                    #game.mode = "custom"


if __name__ == '__main__':
    main()
