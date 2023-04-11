from pieces import *
import pygame
pygame.init()

#chess board - using a 2d array to store the empty squares / pieces
class Board:
    def __init__(self):
        self.array = [[0 for i in range(8)] for j in range(8)]

    def create(self, player):
        self.array[0][0] = Rook("b", 5)
        self.array[0][1] = Knight("b", 3)
        self.array[0][2] = Bishop("b", 3)
        self.array[0][3] = Queen("b", 9)
        self.array[0][4] = King("b", None)
        self.array[0][5] = Bishop("b", 3)
        self.array[0][6] = Knight("b", 3)
        self.array[0][7] = Rook("b", 5)

        self.array[1][0] = Pawn("b", 1)
        self.array[1][1] = Pawn("b", 1)
        self.array[1][2] = Pawn("b", 1)
        self.array[1][3] = Pawn("b", 1)
        self.array[1][4] = Pawn("b", 1)
        self.array[1][5] = Pawn("b", 1)
        self.array[1][6] = Pawn("b", 1)
        self.array[1][7] = Pawn("b", 1)

        self.array[6][0] = Pawn("w", 1)
        self.array[6][1] = Pawn("w", 1)
        self.array[6][2] = Pawn("w", 1)
        self.array[6][3] = Pawn("w", 1)
        self.array[6][4] = Pawn("w", 1)
        self.array[6][5] = Pawn("w", 1)
        self.array[6][6] = Pawn("w", 1)
        self.array[6][7] = Pawn("w", 1)
            
        self.array[7][0] = Rook("w", 5)
        self.array[7][1] = Knight("w", 3)
        self.array[7][2] = Bishop("w", 3)
        self.array[7][3] = Queen("w", 9)
        self.array[7][4] = King("w", None)
        self.array[7][5] = Bishop("w", 3)
        self.array[7][6] = Knight("w", 3)
        self.array[7][7] = Rook("w", 5)


    def display(self, window, theme):
        themes = [[(251, 214, 172), (122, 40, 6)], [(255, 255, 255), (90, 90, 90)], [(250, 245, 220), (77, 160, 44)]]
        for i in range(8):
            for j in range(8):
                if (2 + i + j) % 2 == 0:
                    color = themes[theme][0]
                else:
                    color = themes[theme][1]
                x = j * 75
                y = i * 75
                pygame.draw.rect(window, color, (x, y, 75, 75))
