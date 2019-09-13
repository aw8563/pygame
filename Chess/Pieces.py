import pygame
from abc import ABC, abstractmethod


class Piece(ABC):

    def __init__(self,board, row, col, colour):
        self.board = board
        self.colour = colour
        self.row = row
        self.col = col

        self.grid = 60
        self.x = self.col*self.grid + self.grid//2
        self.y = self.row*self.grid + self.grid//2

        self.moves = []
        self.image = pygame.image.load(self.imageName())




    def validCoord(self, row, col):

        if row < 0 or row > 7:
            return False

        if col < 0 or col > 7:
            return False

        return True

    @abstractmethod 
    def imageName(self):
        pass


    @abstractmethod
    def getMoves(self, king, coord = None):
        pass

    def draw(self, grid, window, perspective):
        if perspective == "W":
            window.blit(self.image, (self.x, self.y, grid, grid))
        else:
            window.blit(self.image, (self.x, grid*8 - self.y, grid, grid))

    # adjusts to the correct square after dragging and dropping
    def fit(self):

        row = (self.y)//self.grid
        col = (self.x)//self.grid

        if (row < 0):
            row = 0

        if col < 0:
            col = 0

        if row > 7:
            row = 7

        if col > 7:
            col = 7

        return row,col

    def reset(self):
        self.x = self.col*self.grid + self.grid//2
        self.y = self.row*self.grid + self.grid//2   

    def moveTo(self, newRow, newCol):

        self.board[self.row][self.col] = None
        
        self.row = newRow
        self.col = newCol

        self.board[self.row][self.col] = self
        
        self.x = self.col*self.grid + self.grid//2
        self.y = self.row*self.grid + self.grid//2   


class Pawn(Piece):
    def __init__(self,board, row, col, colour):
        Piece.__init__(self,board,row,col,colour)
        self.starting = True
        self.enPassant = False



    def getMoves(self, king, coord = None):
        result = []
        direction = 1
        temp = None


        if coord == None:
            row = self.row
            col = self.col
        else:
            row = coord[0]
            col = coord[1]
            temp = self.board[row][col]
            self.board[self.row][self.col] = None
            self.board[row][col] = self



        if (self.colour == "W"):
            direction = -1

        if row + direction >= 0 and row + direction <= 7: 

            newRow = row + direction
            newCol = col
            
            piece = self.board[newRow][newCol]
            if piece == None:

                # make sure king is not in check here 

                self.board[newRow][newCol] = self
                self.board[self.row][self.col] = None



                if not (king.inCheck(king.row, king.col)):
                    result.append((newRow, newCol)) 



                self.board[self.row][self.col] = self
                self.board[newRow][newCol] = piece

                # self.board[self.row][self.col] = self
        

        if (self.starting and self.board[row + 2*direction][col] == None):

            self.board[row + 2*direction][col] = self
            self.board[self.row][self.col] = None

            if not (king.inCheck(king.row, king.col)):
                result.append((row + 2*direction, col)) 

            self.board[self.row][self.col] = self
            self.board[row + 2*direction][col] = None


        # check captures
        captures = [[direction, -1], [direction, 1]]

        for capture in captures:
            newRow = row + capture[0]
            newCol = col + capture[1]

            if not self.validCoord(newRow,newCol):
                continue

            piece = self.board[newRow][newCol]
            if self.board[newRow][newCol] != None and self.board[newRow][newCol].colour != self.colour:

                self.board[newRow][newCol] = self
                self.board[self.row][self.col] = None

                if not (king.inCheck(king.row, king.col)):
                    result.append((newRow, newCol)) 

                self.board[self.row][self.col] = self
                self.board[newRow][newCol] = piece             


        # handle enpassant
        captures = [[0,1],[0,-1]]

        for capture in captures:
            newRow = row + capture[0]
            newCol = col + capture[1]

            if not self.validCoord(newRow,newCol):
                continue

            piece = self.board[newRow][newCol]
            if (piece != None and isinstance(piece, Pawn) and piece.colour != self.colour):
                if (self.colour == 'W' and self.row == 3) or (self.colour == 'B' and self.row == 4):
                    if (piece.enPassant):


                        self.board[newRow][newCol] = self
                        self.board[self.row][self.col] = None

                        if not (king.inCheck(king.row, king.col)):
                            result.append((newRow + direction, newCol)) 

                        self.board[self.row][self.col] = self
                        self.board[newRow][newCol] = piece     

        if coord != None:
            self.board[self.row][self.col] = self
            self.board[row][col] = temp
        return result

    def moveTo(self, newRow, newCol):
    


        self.board[self.row][self.col] = None
        
        self.row = newRow
        self.col = newCol

        capture = self.board[newRow][newCol]
        if (self.board[self.row][self.col] == None):
            # we enpassant here
            direction = 1
            if (self.colour == 'B'):
                direction = -1

            capture = self.board[self.row + direction][self.col]
            self.board[self.row + direction][self.col] = None

        if capture != None:
            capture.row = -1
            capture.col = -1



        self.board[self.row][self.col] = self
        
        self.x = self.col*self.grid + self.grid//2
        self.y = self.row*self.grid + self.grid//2   


     

        if (self.starting and (self.row == 3 or self.row == 4)):
            self.enPassant = True
        else:
            self.enPassant = False

        self.starting = False



        if (self.row == 0 or self.row == 7):
            self.board[self.row][self.col] = Queen(self.board, self.row, self.col, self.colour)


    def imageName(self):
        string = 'models/'

        if self.colour == 'W':
            string += 'white'
        else:
            string += 'black'

        string += 'Pawn'
        string += '.png'
        return string

    def __str__(self):
        return self.colour + " pn"

class Knight(Piece):
    def __init__(self,board, row, col, colour):
        Piece.__init__(self,board,row,col,colour)

    def imageName(self):
        string = 'models/'

        if self.colour == 'W':
            string += 'white'
        else:
            string += 'black'

        string += 'Knight'
        string += '.png'
        return string

    def getMoves(self, king, coord = None):
        temp = None
        if coord == None:
            row = self.row
            col = self.col
        else:
            row = coord[0]
            col = coord[1]
            self.board[self.row][self.col] = None
            temp = self.board[row][col]
            self.board[row][col] = self

        if (row == None):
            row = self.row

        if (col == None):
            col = self.col

        result = []
        moves = [[1,2], [1,-2], [2,1], [2,-1], [-1,-2], [-2,-1], [-1,2], [-2,1]]
        for move in moves:
            newRow = row + move[0]
            newCol = col + move[1]

            # if newRow < 0 or newRow >= 7:
            #     continue

            # if newCol < 0 or newCol >= 7:
            #     continue
            if not (self.validCoord(newRow, newCol)):
                continue

            piece = self.board[newRow][newCol]
            if piece == None or piece.colour != self.colour:

                # make sure king is not in check here 
                self.board[newRow][newCol] = self
                self.board[self.row][self.col] = None

                if not (king.inCheck(king.row, king.col)):
                    result.append((newRow, newCol))

                self.board[self.row][self.col] = self
                self.board[newRow][newCol] = piece


        if coord != None:
            self.board[self.row][self.col] = self
            self.board[row][col] = temp
        return result

    def __str__(self):
        return self.colour + " kn"

class Rook(Piece):
    def __init__(self,board, row, col, colour):
        Piece.__init__(self,board,row,col,colour)

    def imageName(self):
        string = 'models/'

        if self.colour == 'W':
            string += 'white'
        else:
            string += 'black'

        string += 'Rook'
        string += '.png'
        return string

    def getMoves(self, king, coord = None):
        temp = None
        if coord == None:
            row = self.row
            col = self.col
        else:
            row = coord[0]
            col = coord[1]

            temp = self.board[row][col]

            self.board[self.row][self.col] = None
            self.board[row][col] = self


        if (row == None):
            row = self.row

        if (col == None):
            col = self.col

        result = []
        directions = [[0, 1], [0, -1], [1,0], [-1,0]]

        for direction in directions:
            newRow = row
            newCol = col
            while (True):
                newRow += direction[0]
                newCol += direction[1]
            
                if not self.validCoord(newRow, newCol):
                    break

                piece = self.board[newRow][newCol]
                if piece != None:
                    if piece.colour != self.colour:

                        # make sure king is not in check here 
                        self.board[newRow][newCol] = self
                        self.board[self.row][self.col] = None

                        if not (king.inCheck(king.row, king.col)):
                            result.append((newRow, newCol))

                        self.board[self.row][self.col] = self
                        self.board[newRow][newCol] = piece
                    break
                else:
                    self.board[newRow][newCol] = self
                    self.board[self.row][self.col] = None
                    if not (king.inCheck(king.row, king.col)):
                        result.append((newRow, newCol))                   
                    self.board[self.row][self.col] = self
                    self.board[newRow][newCol] = piece

        if coord != None:
            self.board[self.row][self.col] = self
            self.board[row][col] = temp
        return result
        
    def moveTo(self, newRow, newCol):

        if self.row == 0 and self.col == 0: # black long

            king = self.board[0][4]
            if isinstance(king, King):
                king.castleLong = False

        elif self.row == 0 and self.col == 7: # black short

            king = self.board[0][4]
            if isinstance(king, King):
                king.castleShort = False      

        elif self.row == 7 and self.col == 0: # white long

            king = self.board[7][4]
            if isinstance(king, King):
                king.castleLong = False

        elif self.row == 7 and self.col == 7: # white short
            king = self.board[7][4]
            if isinstance(king, King):
                king.castleShort = False        

        self.board[self.row][self.col] = None
            
        self.row = newRow
        self.col = newCol

        self.board[self.row][self.col] = self
        
        self.x = self.col*self.grid + self.grid//2
        self.y = self.row*self.grid + self.grid//2   


    def __str__(self):
        return self.colour + " rk"

class Bishop(Piece):
    def __init__(self,board, row, col, colour):
        Piece.__init__(self,board,row,col,colour)

    def imageName(self):
        string = 'models/'

        if self.colour == 'W':
            string += 'white'
        else:
            string += 'black'

        string += 'Bishop'
        string += '.png'
        return string

    def getMoves(self, king, coord = None):
        temp = None
        if coord == None:
            row = self.row
            col = self.col
        else:
            row = coord[0]
            col = coord[1]
            self.board[self.row][self.col] = None
            temp = self.board[row][col]
            self.board[row][col] = self

        if (row == None):
            row = self.row

        if (col == None):
            col = self.col

        result = []
        directions = [[1, 1], [1, -1], [-1,1], [-1,-1]]

        for direction in directions:
            newRow = row
            newCol = col
            while (True):
                newRow += direction[0]
                newCol += direction[1]
            
                if not self.validCoord(newRow, newCol):
                    break


                piece = self.board[newRow][newCol]
                if piece != None:
                    if piece.colour != self.colour:

                        # make sure king is not in check here 
                        self.board[newRow][newCol] = self
                        self.board[self.row][self.col] = None

                        if not (king.inCheck(king.row, king.col)):
                            result.append((newRow, newCol))

                        self.board[self.row][self.col] = self
                        self.board[newRow][newCol] = piece
                    break
                else:
                    self.board[newRow][newCol] = self
                    self.board[self.row][self.col] = None
                    if not (king.inCheck(king.row, king.col)):
                        result.append((newRow, newCol))                   
                    self.board[self.row][self.col] = self
                    self.board[newRow][newCol] = piece

        if coord != None:
            self.board[self.row][self.col] = self
            self.board[row][col] = temp

        return result

    def __str__(self):
        return self.colour + " bp"

class Queen(Piece):
    def __init__(self,board, row, col, colour):
        Piece.__init__(self,board,row,col,colour)

    def imageName(self):
        string = 'models/'

        if self.colour == 'W':
            string += 'white'
        else:
            string += 'black'

        string += 'Queen'
        string += '.png'
        return string

    def getMoves(self, king, coord = None):
        temp = None
        if coord == None:
            row = self.row
            col = self.col
        else:
            row = coord[0]
            col = coord[1]
            self.board[self.row][self.col] = None
            temp = self.board[row][col]
            self.board[row][col] = self

        if (row == None):
            row = self.row

        if (col == None):
            col = self.col

        result = []
        directions = [[1, 1], [1, -1], [-1,1], [-1,-1], [0, 1], [0, -1], [1,0], [-1,0]]


        for direction in directions:
            newRow = row
            newCol = col
            while (True):
                newRow += direction[0]
                newCol += direction[1]
            
                if not self.validCoord(newRow, newCol):
                    break

                piece = self.board[newRow][newCol]
                if piece != None:
                    if piece.colour != self.colour:

                        # make sure king is not in check here 
                        self.board[newRow][newCol] = self
                        self.board[self.row][self.col] = None

                        if not (king.inCheck(king.row, king.col)):
                            result.append((newRow, newCol))

                        self.board[self.row][self.col] = self
                        self.board[newRow][newCol] = piece
                    break
                else:
                    self.board[newRow][newCol] = self
                    self.board[self.row][self.col] = None
                    if not (king.inCheck(king.row, king.col)):
                        result.append((newRow, newCol))                   
                    self.board[self.row][self.col] = self
                    self.board[newRow][newCol] = piece

        if coord != None:
            self.board[self.row][self.col] = self
            self.board[row][col] = temp

        return result
        
    def __str__(self):
        return self.colour + " qn"

class King(Piece):
    def __init__(self,board,row, col, colour):
        Piece.__init__(self,board,row,col,colour)

        self.castleLong = True
        self.castleShort = True

    # returns empty list if king is not in check,
    # otherwise return list of squares that will block the check

    def imageName(self):
        string = 'models/'

        if self.colour == 'W':
            string += 'white'
        else:
            string += 'black'

        string += 'King'
        string += '.png'
        return string

    def getMoves(self, king, coord = None):
        temp = None
        if coord == None:
            row = self.row
            col = self.col
        else:
            row = coord[0]
            col = coord[1]
            self.board[self.row][self.col] = None
            temp = self.board[row][col]
            self.board[row][col] = self

        if (row == None):
            row = self.row

        if (col == None):
            col = self.col

        result = []
        moves = [[1, 1], [1, -1], [-1,1], [-1,-1], [0, 1], [0, -1], [1,0], [-1,0]]

        for move in moves:
            newRow = row + move[0]
            newCol = col + move[1]

            if not (self.validCoord(newRow, newCol)):
                continue


            piece = self.board[newRow][newCol]
            if piece == None or piece.colour != self.colour:

                # make sure king is not in check here 
                self.board[newRow][newCol] = self
                self.board[self.row][self.col] = None



                if not (self.inCheck(newRow, newCol)):
                    result.append((newRow, newCol))

                self.board[self.row][self.col] = self
                self.board[newRow][newCol] = piece



            # need to make sure no check in this position

        if coord != None:
            self.board[self.row][self.col] = self
            self.board[row][col] = temp



        if self.castleShort:
            clear = True
            for i in range(1,3):
                # check that each square is not a check 
                if (self.board[self.row][self.col + i] == None):
                    self.board[self.row][self.col + i] = self
                    if (self.inCheck(self.row, self.col + i)):
                        clear = False

                    self.board[self.row][self.col + i] = None

                else:
                    clear = False


            if (clear):
                result.append((self.row, self.col + 2))


        if self.castleLong:
            clear = True
            for i in range(1,4):
                # check that each square is not a check 
                if (self.board[self.row][self.col - i] == None):
                    self.board[self.row][self.col - i] = self
                    if (self.inCheck(self.row, self.col - i)):
                        clear = False

                    self.board[self.row][self.col - i] = None

                else:
                    clear = False


            if (clear):
                result.append((self.row, self.col - 2))

            # check long castle
        return result

    def moveTo(self, newRow, newCol):

        self.board[self.row][self.col] = None
        
        
        if self.col - newCol < -1: # castled short
            self.board[self.row][self.col + 3].moveTo(self.row, self.col + 1)

        if self.col - newCol > 1: # castled long
            self.board[self.row][self.col - 4].moveTo(self.row, self.col - 1)


        self.row = newRow
        self.col = newCol
        self.board[self.row][self.col] = self
        
        self.x = self.col*self.grid + self.grid//2
        self.y = self.row*self.grid + self.grid//2   

        self.castleShort = False
        self.castleLong = False

    def __str__(self):
        return self.colour + " kg"


    def inCheck(self, row, col):
        # check diagonals
        directions = [[1,1], [-1,-1], [1,-1], [-1,1]]
        for direction in directions:
            newRow = row
            newCol = col
            n = 0
            while (True):
                n += 1
                newRow += direction[0]
                newCol += direction[1]
            
                if not self.validCoord(newRow, newCol):
                    break

                piece = self.board[newRow][newCol]
                if piece != None: # found a piece here
                    if piece.colour != self.colour: # enemy piece
                        if isinstance(piece, Bishop) or isinstance(piece, Queen):
                            return True
                        if n == 1 and isinstance(piece, King):
                            return True
                    break

        # check vertical/horizontal
        directions = [[0,1], [0,-1], [1,0], [-1,0]]
        for direction in directions:
            newRow = row
            newCol = col
            n = 0
            while (True):
                n += 1
                newRow += direction[0]
                newCol += direction[1]
            
                if not self.validCoord(newRow, newCol):
                    break

                piece = self.board[newRow][newCol]
                if piece != None: # found a piece here
                    if piece.colour != self.colour: # enemy piece
                        if isinstance(piece, Rook) or isinstance(piece, Queen):
                            return True
                        if n == 1 and isinstance(piece, King):
                            return True

                    break

        # check for knights
        directions = [[1,2], [1,-2], [2,1], [2,-1], [-1,-2], [-2,-1], [-1,2], [-2,1]]
        for direction in directions:
            newRow = row + direction[0]
            newCol = col + direction[1]
            

            if not self.validCoord(newRow, newCol):
                continue
            
            piece = self.board[newRow][newCol]


            if piece != None and piece.colour != self.colour and isinstance(piece, Knight):
                return True


        # check for pawns 
        directions = [[-1,1], [-1,-1]] #white

        if self.colour == 'B': #black
            directions = [[1,1],[1,-1]]
        
        for direction in directions:
            newRow = row + direction[0]
            newCol = col + direction[1]

        
            if not self.validCoord(newRow, newCol):
                continue

            piece = self.board[newRow][newCol]

            if piece != None and piece.colour != self.colour and isinstance(piece, Pawn):
                return True

        # pass all checks return true 
        return False