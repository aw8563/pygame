import pygame

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


class Pawn(Piece):
    def __init__(self, grid, colour, pieceType, x, y):
        Piece.__init__(self, grid, colour, pieceType, x, y)

    def isValidMove(self, board, x, y):

        coord = [0,0]
        coord[1] = ord(self.coord[0]) - ord('A')
        coord[0] = 8 - self.coord[1]

        row = coord[0]
        col = coord[1]

        if self.colour == 'W': # white pawn

            if board[row - 1][col] == None: # nothing in front of it

                r = [chr(col + ord('A')), 8 - (row - 1)]   
                if x == r[0] and y == r[1]:
                    return True 

                if row == 6 and board[row - 2][col] == None: # starting position and 2 moves ahead are empty
                    r = [chr(col + ord('A')), 8 - (row - 2)]
                    if x == r[0] and y == r[1]:
                        return True
            # taking diagonally
            if (row > 0): # not last rank
                if col + 1 < 8 and board[row - 1][col + 1] != None and board[row - 1][col + 1].colour == "B":
                    r = [chr(col + 1 + ord('A')), 8 - (row - 1)]
                    if x == r[0] and y == r[1]:
                        return True


                if col - 1 >= 0 and board[row - 1][col - 1] != None and board[row - 1][col - 1].colour == "B":
                    r = [chr(col - 1 + ord('A')), 8 - (row - 1)]
                    if x == r[0] and y == r[1]:
                        return True
        elif self.colour == 'B': # black pawn

            if board[row + 1][col] == None: # nothing in front of it
                # print('made it here')
                r = [chr(col + ord('A')), 8 - (row + 1)] 
                if x == r[0] and y == r[1]:
                        return True

                # print(row + 2, col, board[row + 1][col])
                if row == 1 and board[row + 2][col] == None: # starting position and 2 moves ahead are empty
                    # print("JDSKLF")
                    r = [chr(col + ord('A')), 8 - (row + 2)]   
                    if x == r[0] and y == r[1]:
                        return True
            if (row < 7): # not last rank
                if col + 1 < 8 and board[row + 1][col + 1] != None and board[row + 1][col + 1].colour == "W":
                    r = [chr(col + 1 + ord('A')), 8 - (row + 1)]   
                    if x == r[0] and y == r[1]:
                        return True
                if col - 1 >= 0 and board[row + 1][col - 1] != None and board[row + 1][col - 1].colour == "W":
                    r = [chr(col - 1 + ord('A')), 8 - (row + 1)]
                    if x == r[0] and y == r[1]:
                        return True
        return False

class Bishop(Piece):
    def __init__(self, grid, colour, pieceType, x, y):
        Piece.__init__(self, grid, colour, pieceType, x, y)

    def isValidMove(self, board, x, y):
        coord = [0,0]
        coord[1] = ord(self.coord[0]) - ord('A')
        coord[0] = 8 - self.coord[1]

        row = coord[0] - 1
        col = coord[1] + 1

        while (row >= 0 and col < 8):

            move = [0,0]
            move[0] = chr(col + ord('A'))
            move[1] = 8 - row

            if (board[row][col] == None):    
                if x == move[0] and y == move[1]:
                    return True
            elif (board[row][col].colour != self.colour):
                if x == move[0] and y == move[1]:
                    return True
                break
            else:
                break

            row -= 1
            col += 1

        row = coord[0] + 1
        col = coord[1] + 1

        while (row < 8 and col < 8):
            move = [0,0]
            move[0] = chr(col + ord('A'))
            move[1] = 8 - row
            if (board[row][col] == None):    
                if x == move[0] and y == move[1]:
                    return True
            elif (board[row][col].colour != self.colour):
                if x == move[0] and y == move[1]:
                    return True
                break
            else:
                break

            row += 1
            col += 1

        row = coord[0] - 1
        col = coord[1] - 1
        while (row >= 0 and col >= 0):
            move = [0,0]
            move[0] = chr(col + ord('A'))
            move[1] = 8 - row
            if (board[row][col] == None):    
                if x == move[0] and y == move[1]:
                    return True
            elif (board[row][col].colour != self.colour):
                if x == move[0] and y == move[1]:
                    return True
                break
            else:
                break

            row -= 1
            col -= 1

        row = coord[0] + 1
        col = coord[1] - 1
        while (row < 8 and col >= 0):
            move = [0,0]
            move[0] = chr(col + ord('A'))
            move[1] = 8 - row
            if (board[row][col] == None):    
                if x == move[0] and y == move[1]:
                    return True
            elif (board[row][col].colour != self.colour):
                if x == move[0] and y == move[1]:
                    return True
                break
            else:
                break

            row += 1
            col -= 1

        return False

class Knight(Piece):
    def __init__(self, grid, colour,pieceType, x, y):
        Piece.__init__(self, grid, colour, pieceType, x, y)


    def isValidMove(self, board, x, y):
        coord = [0,0]
        coord[1] = ord(self.coord[0]) - ord('A')
        coord[0] = 8 - self.coord[1]

        results = []

        row = coord[0]
        col = coord[1]

        moves = [[1,2], [1,-2], [2,1], [2,-1], [-1,-2], [-2,-1], [-1,2], [-2,1]]
        
        for pair in moves:
            row = coord[0] + pair[0]
            col = coord[1] + pair[1]


            move = [0,0]
            move[0] = chr(col + ord('A'))
            move[1] = 8 - row
            if (row >= 0 and col >= 0 and row < 8 and col < 8):
                if (board[row][col] == None):    
                    if x == move[0] and y == move[1]:
                        return True
                elif (board[row][col].colour != self.colour):
                    if x == move[0] and y == move[1]:
                        return True

        return False




class Rook(Piece):
    def __init__(self, grid, colour,pieceType, x, y):
        Piece.__init__(self, grid, colour, pieceType, x, y)

    def isValidMove(self, board, x, y):
        coord = [0,0]
        coord[1] = ord(self.coord[0]) - ord('A')
        coord[0] = 8 - self.coord[1]


        row = coord[0] - 1
        col = coord[1]

        results = []

        while (row >= 0):
            move = [0,0]
            move[0] = chr(col + ord('A'))
            move[1] = 8 - row
            if (board[row][col] == None):    
                if x == move[0] and y == move[1]:
                    return True
            elif (board[row][col].colour != self.colour):
                if x == move[0] and y == move[1]:
                    return True
                break
            else:
                break

            row -= 1


        row = coord[0] + 1
        col = coord[1]

        while (row < 8):
            move = [0,0]
            move[0] = chr(col + ord('A'))
            move[1] = 8 - row
            if (board[row][col] == None):    
                if x == move[0] and y == move[1]:
                    return True
            elif (board[row][col].colour != self.colour):
                if x == move[0] and y == move[1]:
                    return True
                break
            else:
                break

            row += 1


        row = coord[0]
        col = coord[1] - 1
        while (col >= 0):
            move = [0,0]
            move[0] = chr(col + ord('A'))
            move[1] = 8 - row
            if (board[row][col] == None):    
                if x == move[0] and y == move[1]:
                    return True
            elif (board[row][col].colour != self.colour):
                if x == move[0] and y == move[1]:
                    return True
                break
            else:
                break

            col -= 1

        row = coord[0]
        col = coord[1] + 1
        while (col < 8):
            move = [0,0]
            move[0] = chr(col + ord('A'))
            move[1] = 8 - row
            if (board[row][col] == None):    
                if x == move[0] and y == move[1]:
                    return True
            elif (board[row][col].colour != self.colour):
                if x == move[0] and y == move[1]:
                    return True
                break
            else:
                break

            col += 1
            
        return results



class Queen(Piece):
    def __init__(self, grid, colour, pieceType, x, y):
        Piece.__init__(self, grid, colour, pieceType, x, y)

    def isValidMove(self, board, x, y):
        rook = Rook(self.grid, self.colour, "Rook", self.coord[0], self.coord[1])
        bishop = Bishop(self.grid, self.colour, "Bishop", self.coord[0], self.coord[1])

        if bishop.isValidMove(board, x,y):
            return True

        if rook.isValidMove(board,x,y):
            return True        
        # results.append(rook.getLegalMoves(board))
        # results.append(bishop.getLegalMoves(board))

        return False

class King(Piece):
    def __init__(self, grid, colour, pieceType, x, y):
        Piece.__init__(self,grid, colour, pieceType, x, y)

    def isValidMove(self, board, x, y):
        coord = [0,0]
        coord[1] = ord(self.coord[0]) - ord('A')
        coord[0] = 8 - self.coord[1]

        results = []

        row = coord[0]
        col = coord[1]

        moves = [[1,0], [1,1], [0,1], [0,-1], [-1,0], [-1,-1], [-1,1], [1,-1]]
        
        # castling

        for pair in moves:
            row = coord[0] + pair[0]
            col = coord[1] + pair[1]


            move = [0,0]
            move[0] = chr(col + ord('A'))
            move[1] = 8 - row
            if (row >= 0 and col >= 0 and row < 8 and col < 8):
                if (board[row][col] == None):    
                    if x == move[0] and y == move[1]:
                        return True
                elif (board[row][col].colour != self.colour):
                    if x == move[0] and y == move[1]:
                        return True

        # castling

        row = 7 # white king
        if self.colour == 'B': # black king
            row = 0

        if coord[0] == row and coord[1] == 4: # white king
            if x == 'G': # kingside
                blocked = False
                if board[row][5] == None and board[row][6] == None:
                    return 'kingCastle'

            if x == 'C': # queenside
                if board[row][1] == None and board[row][2] == None and board[row][3] == None:
                    return 'queenCastle'


        return False
