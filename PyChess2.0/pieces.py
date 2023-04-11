import pygame

#super class for all pieces
class Piece:
    def __init__(self, color, rank):
        self.color = color
        self.rank = rank
        self.width = self.image.get_size()[0]
        self.height = self.image.get_size()[1]
        self.selected = False
        self.validPos = []


class King(Piece):
    def __init__(self, color, rank):
        self.image = pygame.image.load(f"Assets/Images/{color}k.png")
        Piece.__init__(self, color, rank)
        self.firstMove = True

    def checkValidMoves(self, row, col, board):
        self.validPos.clear()
        offset = [[1, 1], [1, -1], [-1, -1], [-1, 1], [1, 0], [-1, 0], [0, -1], [0, 1]]
        for i in range(len(offset)):
            newRow = row
            newCol = col
            if newRow + offset[i][0] > -1 and newRow + offset[i][0] < 8 and newCol + offset[i][1] > -1 and newCol + offset[i][1] < 8:
                newRow += offset[i][0]
                newCol += offset[i][1]
                square = board[newRow][newCol]
                if self.noSurroundingKing(newRow, newCol, board):
                    if square == 0:
                        self.validPos.append([newRow, newCol])
                    elif square != 0 and square.color != self.color:
                        self.validPos.append([newRow, newCol])

    def noSurroundingKing(self, row, col, board):
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i > -1 and i < 8 and j > -1 and j < 8:
                    piece = board[i][j]
                    if piece != 0 and piece.rank == None and piece.color != self.color:
                        return False
        return True

                    

class Queen(Piece):
    def __init__(self, color, rank):
        self.image = pygame.image.load(f"Assets/Images/{color}q.png")
        Piece.__init__(self, color, rank)

    def checkValidMoves(self, row, col, board):
        self.validPos.clear()
        offset = [[1, 1], [1, -1], [-1, -1], [-1, 1], [1, 0], [-1, 0], [0, -1], [0, 1]]
        for i in range(len(offset)):
            newRow = row
            newCol = col
            while True:
                if newRow + offset[i][0] > -1 and newRow + offset[i][0] < 8 and newCol + offset[i][1] > -1 and newCol + offset[i][1] < 8:
                    newRow += offset[i][0]
                    newCol += offset[i][1]
                    square = board[newRow][newCol]
                    if square == 0:
                        self.validPos.append([newRow, newCol])
                    elif square != 0 and square.color != self.color:
                        self.validPos.append([newRow, newCol])
                        break
                    else:
                        break
                else:
                    break

class Rook(Piece):
    def __init__(self, color, rank):
        self.image = pygame.image.load(f"Assets/Images/{color}r.png")
        Piece.__init__(self, color, rank)
        self.firstMove = True

    def checkValidMoves(self, row, col, board):
        self.validPos.clear()
        offset = [[1, 0], [-1, 0], [0, -1], [0, 1]]
        for i in range(len(offset)):
            newRow = row
            newCol = col
            while True:
                if newRow + offset[i][0] > -1 and newRow + offset[i][0] < 8 and newCol + offset[i][1] > -1 and newCol + offset[i][1] < 8:
                    newRow += offset[i][0]
                    newCol += offset[i][1]
                    square = board[newRow][newCol]
                    if square == 0:
                        self.validPos.append([newRow, newCol])
                    elif square != 0 and square.color != self.color:
                        self.validPos.append([newRow, newCol])
                        break
                    else:
                        break
                else:
                    break

                
class Bishop(Piece):
    def __init__(self, color, rank):
        self.image = pygame.image.load(f"Assets/Images/{color}b.png")
        Piece.__init__(self, color, rank)

    def checkValidMoves(self, row, col, board):
        self.validPos.clear()
        offset = [[1, 1], [1, -1], [-1, -1], [-1, 1]]
        for i in range(len(offset)):
            newRow = row
            newCol = col
            while True:
                if newRow + offset[i][0] > -1 and newRow + offset[i][0] < 8 and newCol + offset[i][1] > -1 and newCol + offset[i][1] < 8:
                    newRow += offset[i][0]
                    newCol += offset[i][1]
                    square = board[newRow][newCol]
                    if square == 0:
                        self.validPos.append([newRow, newCol])
                    elif square != 0 and square.color != self.color:
                        self.validPos.append([newRow, newCol])
                        break
                    else:
                        break
                else:
                    break


class Knight(Piece):
    def __init__(self, color, rank):
        self.image = pygame.image.load(f"Assets/Images/{color}n.png")
        Piece.__init__(self, color, rank)

    def checkValidMoves(self, row, col, board):
        self.validPos.clear()
        offset = [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2]]
        for i in range(len(offset)):
            if row + offset[i][0] > -1 and row + offset[i][0] < 8 and col + offset[i][1] > -1 and col + offset[i][1] < 8:
                newRow = row + offset[i][0]
                newCol = col + offset[i][1]
                square = board[newRow][newCol]
                if (square != 0 and square.color != self.color) or square == 0:
                    self.validPos.append([newRow, newCol])

            
class Pawn(Piece):
    def __init__(self, color, rank):
        self.image = pygame.image.load(f"Assets/Images/{color}p.png")
        Piece.__init__(self, color, rank)
        self.firstMove = True

    def checkValidMoves(self, row, col, board):
        self.validPos.clear()
        if self.color == "w":
            try:
                newRow = row - 1
                newCol = col + 0
                square = board[newRow][newCol]
                if square == 0:
                    self.validPos.append([newRow, newCol])
                newRow = row - 1
                newCol = col + 1
                if newCol < 8:
                    square = board[newRow][newCol]
                    if square != 0 and square.color != self.color:
                        self.validPos.append([newRow, newCol])
                newRow = row - 1
                newCol = col - 1
                if newCol > -1:
                    square = board[newRow][newCol]
                    if square != 0 and square.color != self.color:
                        self.validPos.append([newRow, newCol])
                if self.firstMove:
                    newRow = row - 2
                    newCol = col + 0
                    if newRow < 8:
                        square = board[newRow][newCol]
                        if square == 0 and board[newRow + 1][newCol] == 0:
                            self.validPos.append([newRow, newCol])
            except:
                pass
        else:
            try:
                newRow = row + 1
                newCol = col + 0
                square = board[newRow][newCol]
                if square == 0:
                    self.validPos.append([newRow, newCol])
                newRow = row + 1
                newCol = col + 1
                if newCol < 8:
                    square = board[newRow][newCol]
                    if square != 0 and square.color != self.color:
                        self.validPos.append([newRow, newCol])
                newRow = row + 1
                newCol = col - 1
                if newCol > -1:
                    square = board[newRow][newCol]
                    if square != 0 and square.color != self.color:
                        self.validPos.append([newRow, newCol])

                if self.firstMove:
                    newRow = row + 2
                    newCol = col + 0
                    if newRow < 8:
                        square = board[newRow][newCol]
                        if square == 0 and board[newRow - 1][newCol] == 0:
                            self.validPos.append([newRow, newCol])
            except:
                pass
    
