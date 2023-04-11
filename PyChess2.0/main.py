import pygame, socket, sys, pickle, threading, time
from pieces import *
from board import *


pygame.init()
window = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
font1 = pygame.font.SysFont("calibri", 70, True)
font2 = pygame.font.SysFont("calibri", 40, True)
font3 = pygame.font.SysFont("calibri", 100, True)
font4 = pygame.font.SysFont("calibri", 55, True)


class Game:
    def __init__(self):
        self.running = False
        self.state = "playing"
        self.theme = 2
        self.moveSFX = pygame.mixer.Sound("Assets/Audio/move.wav")
        self.checkSFX = pygame.mixer.Sound("Assets/Audio/check.wav")
        self.captureSFX = pygame.mixer.Sound("Assets/Audio/capture.wav")
        self.checkmateSFX = pygame.mixer.Sound("Assets/Audio/checkmate.wav")
        self.playerPieces = []
        self.opponentPieces = []

    #confirmation from server to start the game
    def receiveStart(self):
        self.running = client.receive()

    #main game loop
    def run(self):
        while True:
            self.input()
            self.render()
            self.update()

    #gathering the player's and opponent's piecees
    def gatherPieces(self):
        for i in range(8):
            for j in range(8):
                piece = board.array[i][j]
                if piece == 0:
                    pass
                elif piece.color == player.color:
                    self.playerPieces.append(piece)
                else:
                    self.opponentPieces.append(piece)

    #handling user input
    def input(self):
        dragger.update(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.theme -= 1
            if player.turn and self.state == "playing":
                player.selectPiece(event)
                player.releasePiece(event)
            if self.theme == -1:
                self.theme = 2

    #rendering objects to the screen
    def render(self):
        board.display(window, self.theme)
        if player.color == "w":
            self.highlightSquare("w")
            self.displayPiece("w")
        else:
            self.highlightSquare("b")
            self.displayPiece("b")
        self.endMessage()

    #displaying text to the screen
    def displayText(self, font, message, x, y):
        text = font.render(message, True, (0, 0, 0))
        window.blit(text, (x, y))
        
    #;highlighting all valid moves for a specific piece
    def highlightSquare(self, color):
        if dragger.selectedPiece != 0 and dragger.selectedPiece.selected:
            for i in range(len(dragger.selectedPiece.validPos)):
                coords = dragger.selectedPiece.validPos[i]
                if color == "w":
                    row = coords[0]
                    col = coords[1]
                else:
                    row = 7 - coords[0]
                    col = 7 - coords[1]
                x = col * 75
                y = row * 75
                pygame.draw.rect(window, (180, 255, 180), (x, y, 75, 75))

    #displaying the pieces to the screen
    def displayPiece(self, color):
        for i in range(8):
            for j in range(8):
                piece = board.array[i][j]
                if piece != 0 and not piece.selected and color == "w":
                    row = i
                    col = j
                    x = 37.5 + col * 75 - piece.width / 2
                    y = 37.5 + row * 75 - piece.height / 2
                    window.blit(piece.image, (x, y))
                elif piece != 0 and not piece.selected and color == "b":
                    row = 7 - i
                    col = 7 - j
                    x = 37.5 + col * 75 - piece.width / 2
                    y = 37.5 + row * 75 - piece.height / 2
                    window.blit(piece.image, (x, y))
                elif piece != 0 and piece.selected:
                    x = dragger.mx - piece.width / 2
                    y = dragger.my - piece.height / 2
                    window.blit(piece.image, (x, y))

    #diplaying a message when the game ends in either a win, loss or draw
    def endMessage(self): 
        if self.state == "playing":
            return
        if self.state == "draw":
            self.displayText(font1, self.message, 230, 230)
            self.displayText(font4, "By Insufficient Material",  30, 310)
        elif self.state == "stalemate":
            self.displayText(font1, self.message, 180, 230)
            self.displayText(font1, "By Stalemate",  100, 310)
        elif game.state == "checkmate":
            self.displayText(font1, self.message, 180, 230)
            self.displayText(font1, "By Checkmate",  100, 310)

    #updating the window
    def update(self):
        pygame.display.update()
        window.fill((0, 0, 0))
        clock.tick(30)

    #looking for the position of the players king
    def lookForKing(self, array):
        for i in range(8):
            for j in range(8):
                piece = array[i][j]
                if piece != 0 and piece.rank == None and piece.color == player.color:
                    return [i, j]

    #making sure that the player's move doesn't cause them to be in check
    def revalidatePositions(self):
        removing = []
        for pos in dragger.selectedPiece.validPos:
            row = pos[0]
            col = pos[1]
            replica = [x[:] for x in board.array]
            replica[dragger.initialRow][dragger.initialCol], replica[row][col] = \
            0, replica[dragger.initialRow][dragger.initialCol]
            
            if player.check(replica):
                removing.append(pos)
                
        for pos in removing:
            dragger.selectedPiece.validPos.remove(pos)

    #making sure that player can only castle if their king and rook will not be underattack afterwards
    def revalidateCastle(self, kingInitialRow, kingIntialCol, kingFinalRow, kingFinalCol, rookInitialRow, rookIntialCol, rookFinalRow, rookFinalCol):
        replica = [x[:] for x in board.array]
        replica[a][b], replica[c][d] = 0, replica[a][b]
        replica[e][f], replica[g][h] = 0, replica[e][f]
        
        if player.check(replica) or player.rookAttack(replica, [g, h]):
            return False
        return True

    #checking for a draw
    def checkDraw(self):
        if ((len(self.playerPieces) == 2 and self.minorPieceLeft(self.playerPieces)) or len(self.playerPieces) == 1) and \
           ((len(self.opponentPieces) == 2 and self.minorPieceLeft(self.opponentPieces)) or len(self.opponentPieces) == 1):
            self.state = "draw"
            self.message = "Draw"
            client.transmit(["draw", "Draw"])

    #checking for minor pieces left 
    def minorPieceLeft(self, array):
        for i in range(len(array)):
            piece = array[i]
            if piece.rank == 3:
                return True
        return False


class Player:
    def __init__(self):
        self.color = client.receive()
        self.turn = client.receive()

    #selecting a piece and checking for all its valid moves
    def selectPiece(self, event):
        if not (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            return
        if player.color == "w":
            row = dragger.my // 75
            col = dragger.mx // 75
        else:
            row = 7 - (dragger.my // 75)
            col = 7 - (dragger.mx // 75)
                    
        dragger.initialCol = col
        dragger.initialRow = row
        piece = board.array[row][col]

        if piece != 0 and piece.color == player.color:
            piece.selected = True
            dragger.selectedPiece = piece
            dragger.selectedPiece.checkValidMoves(dragger.initialRow, dragger.initialCol, board.array)
            game.revalidatePositions()

    #releasing the piece and checking whether it is valid to move or not
    def releasePiece(self, event):
        if not (event.type == pygame.MOUSEBUTTONUP and event.button == 1):
            return
        if player.color == "w":
            row = dragger.my // 75
            col = dragger.mx // 75
        else:
            row = 7 - (dragger.my // 75)
            col = 7 - (dragger.mx // 75)
                    
        dragger.finalCol = col
        dragger.finalRow = row
                
        if dragger.selectedPiece != 0:
            dragger.selectedPiece.selected = False
            if [row, col] in dragger.selectedPiece.validPos:
                player.move()
            elif not player.check(board.array) and dragger.selectedPiece != 0 and \
                dragger.selectedPiece.rank == None and dragger.selectedPiece.firstMove:
                self.castle()

    #castling - both long and short
    def castle(self):
        piece = dragger.selectedPiece
        valid = False
        
        if player.color == "w":
            if board.array[dragger.finalRow][dragger.finalCol] == board.array[7][6] == 0 and \
               board.array[7][7] != 0 and board.array[7][7].rank == 5 and \
               board.array[7][7].firstMove and board.array[7][5] == 0:
                kingInitialRow, kingIntialCol, kingFinalRow, kingFinalCol = dragger.initialRow, dragger.initialCol, dragger.finalRow, dragger.finalCol
                rookInitialRow, rookIntialCol, rookFinalRow, rookFinalCol = 7, 7, 7, 5
                valid = True
            if board.array[dragger.finalRow][dragger.finalCol] == board.array[7][2] == 0 and \
               board.array[7][0] != 0 and board.array[7][0].rank == 5 and \
               board.array[7][0].firstMove and board.array[7][1] == 0 and \
               board.array[7][2] == 0 and board.array[7][3] == 0:
                kingInitialRow, kingIntialCol, kingFinalRow, kingFinalCol = dragger.initialRow, dragger.initialCol, dragger.finalRow, dragger.finalCol
                rookInitialRow, rookIntialCol, rookFinalRow, rookFinalCol = 7, 0, 7, 3
                valid = True
        else:
            if board.array[dragger.finalRow][dragger.finalCol] == board.array[0][6] == 0 and \
               board.array[0][7] != 0 and board.array[0][7].rank == 5 and \
               board.array[0][7].firstMove and board.array[0][5] == 0:
                kingInitialRow, kingIntialCol, kingFinalRow, kingFinalCol = dragger.initialRow, dragger.initialCol, dragger.finalRow, dragger.finalCol
                rookInitialRow, rookIntialCol, rookFinalRow, rookFinalCol = 0, 7, 0, 5
                valid = True
            if board.array[dragger.finalRow][dragger.finalCol] == board.array[0][2] == 0 and \
               board.array[0][0] != 0 and board.array[0][0].rank == 5 and \
               board.array[0][0].firstMove and board.array[0][1] == 0 and \
               board.array[0][2] == 0 and board.array[0][3] == 0:
                kingInitialRow, kingIntialCol, kingFinalRow, kingFinalCol = dragger.initialRow, dragger.initialCol, dragger.finalRow, dragger.finalCol
                rookInitialRow, rookIntialCol, rookFinalRow, rookFinalCol = 0, 0, 0, 3
                valid = True
        if valid:
            if game.revalidateCastle(kingInitialRow, kingIntialCol, kingFinalRow, kingFinalCol, rookInitialRow, rookIntialCol, rookFinalRow, rookFinalCol):
                board.array[kingInitialRow][kingIntialCol], board.array[kingFinalRow][kingFinalCol] = 0, board.array[a][b]
                board.array[e][f], board.array[rookInitialRow][rookIntialCol] = 0, board.array[rookFinalRow][rookFinalCol]
                client.transmit([kingInitialRow, kingIntialCol, kingFinalRow, kingFinalCol])
                client.transmit([rookInitialRow, rookIntialCol, rookFinalRow, rookFinalCol])
                self.turn = False
        
    #moving the piece and sending the move to the server to be sent to the other client
    def move(self):
        if dragger.selectedPiece.rank == 1 and dragger.selectedPiece.firstMove:
            dragger.selectedPiece.firstMove = False
        elif dragger.selectedPiece.rank == 5 and dragger.selectedPiece.firstMove:
            dragger.selectedPiece.firstMove = False
        elif dragger.selectedPiece.rank == None and dragger.selectedPiece.firstMove:
            dragger.selectedPiece.firstMove = False
            
        piece = board.array[dragger.finalRow][dragger.finalCol]
        board.array[dragger.initialRow][dragger.initialCol], board.array[dragger.finalRow][dragger.finalCol] \
        = 0, board.array[dragger.initialRow][dragger.initialCol]
        client.transmit([dragger.initialRow, dragger.initialCol, dragger.finalRow, dragger.finalCol])
        self.turn = False
        
        if piece != 0:
            game.captureSFX.play()
            game.opponentPieces.remove(piece)
        else:
            game.moveSFX.play()
            
        game.checkDraw()
        self.promotePawn()

    #promoting a pawn to a queen
    def promotePawn(self):
        for i in range(8):
            for j in range(8):
                piece = board.array[i][j]
                
                if piece != 0 and piece.color == "w" and piece.rank == 1 and i == 0:
                    board.array[i][j] = Queen("w", 9)
                    piece = board.array[i][j]
                    
                    if player.color == "w":
                        game.playerPieces.append(piece)
                    else:
                        game.opponentPieces.append(piece)
                    
                elif piece != 0 and piece.color == "b" and piece.rank == 1 and i == 7:
                    board.array[i][j] = Queen("b", 9)

    #checking if the rook is under attack after castling
    def rookAttack(self, array, rookPos):
        for i in range(8):
            for j in range(8):
                piece = array[i][j]
                
                if not (piece != 0 and piece.color != player.color):
                    pass
                piece.checkValidMoves(i, j, array)
                
                if rookPos in piece.validPos:
                    return True

    #checking if the king is in check
    def check(self, array):
        for i in range(8):
            for j in range(8):
                kingPos = game.lookForKing(array)
                piece = array[i][j]
                
                if piece != 0 and piece.rank != None and piece.color != player.color:
                    piece.checkValidMoves(i, j, array)
                    
                    if kingPos in piece.validPos:
                        return True

    #checking if the player has no legal moves to protect their king
    def noLegalMoves(self):
        for i in range(8):
            for j in range(8):
                piece = board.array[i][j]

                if piece != 0 and piece.color == player.color:
                    piece.checkValidMoves(i, j, board.array)
                    for pos in piece.validPos:
                        row = pos[0]
                        col = pos[1]
                        replica = [x[:] for x in board.array]
                        replica[i][j], replica[row][col] = 0, replica[i][j]
                        
                        if not self.check(replica):
                            return False
        return True


#class handling client communication with the server
class Client:
    def __init__(self):
        self.PORT = 9998
        self.ADDRESS = "localhost"
        self.ENCODER = "ascii"
        self.socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.socket.connect((self.ADDRESS, self.PORT))

    #sending data over to the server
    def transmit(self, message):
        message = pickle.dumps(message)
        self.socket.send(message)

    #receivin data from the server a
    def receive(self):
        message = pickle.loads(self.socket.recv(1024))
        return message

    #receiving the data from the server which have been sent by the other client
    def receiveMoves(self):
        while True:
            message = self.socket.recv(1048)
            message = pickle.loads(message)
            
            if len(message) == 4:
                piece = board.array[message[2]][message[3]] 
                board.array[message[0]][message[1]], board.array[message[2]][message[3]] = \
                0, board.array[message[0]][message[1]]
                player.turn = True
                player.promotePawn()
                
                if piece != 0:
                    game.captureSFX.play()
                    game.playerPieces.remove(piece)
                else:
                    game.moveSFX.play()
                
                if player.check(board.array) and player.noLegalMoves():
                    game.checkmateSFX.play()
                    game.state = "checkmate"
                    game.message = "You lose"
                    client.transmit(["checkmate", "You win"])
                    
                elif not player.check(board.array) and player.noLegalMoves():
                    game.checkmateSFX.play()
                    game.state = "stalemate"
                    game.message = "Draw"
                    client.transmit(["stalemate", "Draw"])

                elif player.check(board.array):
                    game.checkSFX.play()
                    
            elif len(message) == 2:
                game.state = message[0]
                game.message = message[1]


#class handling the mouse drag
class Dragger:
    def __init__(self):
        self.mx = 0
        self.my = 0
        self.initialCol = 0
        self.initialRow = 0
        self.finalCol = 0
        self.finalRow = 0
        self.selectedPiece = 0

    #updating the dragger's mouse position
    def update(self, mx, my):
        self.mx = mx
        self.my = my
        

#instanciating all objects
game = Game()
dragger = Dragger()
board = Board()
client = Client()
player = Player()

board.create(player)
game.gatherPieces()

image = pygame.image.load("Assets/Images/waiting.jpg")
window.blit(image, (-200, 0))
game.displayText(font3, "CHESS.PY", 100, 50)
game.displayText(font2, "WAITING FOR CONNECTION...", 50, 400)
pygame.display.update()

game.receiveStart()

#starting the game and the client thread
if game.running:
    threading.Thread(target=client.receiveMoves, args=()).start()
    game.run()
