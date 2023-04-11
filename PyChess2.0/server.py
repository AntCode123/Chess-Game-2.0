import socket, pickle, threading, sys

class Server:
    def __init__(self):
        self.PORT = 9998
        self.ADDRESS = "localhost"
        self.ENCODER = "ascii"
        self.socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.socket.bind((self.ADDRESS, self.PORT))
        self.socket.listen()
        self.numberOfClients = 0
        self.clients = []
        self.playerAttributes = [["w", True], ["b", False]]

    def connectClients(self):
        print("Waiting for connections...")
        while self.numberOfClients < 2:
            client, address = self.socket.accept()
            self.clients.append(client)
            self.numberOfClients += 1
            self.sendPlayerAttributes(self.playerAttributes[self.numberOfClients - 1], client)
            threading.Thread(target=self.communication, args=(client, )).start()
            print(f"Client {self.numberOfClients} connected at {address}")
        self.broadcast(True)

    def communication(self, client):
        while True:
            try:
                message = pickle.loads(client.recv(1024))
                self.sendToClient(message, client)
            except:
                return

    def transmit(self, message, client):
        message = pickle.dumps(message)
        client.send(message)

    def broadcast(self, message):
        for socket in self.clients:
            self.transmit(message, socket)

    def sendToClient(self, message, client):
        for socket in self.clients:
            if socket != client:
                self.transmit(message, socket)

    def sendPlayerAttributes(self, attibutes, client):
        self.transmit(attibutes[0], client)
        self.transmit(attibutes[1], client)
            
            
server = Server()
server.connectClients()
