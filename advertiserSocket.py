import socket
import threading

HEADER = 64
PORT = 3595

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
conn = ''


class AdvertiserSocket:
    applicationAvailable = True

    def advertiseApplication(self):
        print("AdvertiseApplication")
        self.applicationAvailable = True
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        SERVER = s.getsockname()[0]
        s.close()
        ADDR = (SERVER, PORT)
        print(f'Python Server address = {SERVER}')
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(ADDR)
        print(f"[LISTENING] Advertiser Server is listening on {SERVER}")
        while self.applicationAvailable:
            server.listen()
            # Accept connections from the outside
            conn, addr = server.accept()
            print("Advertiser Socket ready")




    def stopAdvertisingApplication(self):
        self.applicationAvailable = False
        pass

    def __openSocket(self):
        pass

    def __closeSocket(self):
        pass

    def __sendMsg(self, msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        conn.send(send_length)
        conn.send(message)
        print(conn.recv(64).decode(FORMAT))
        pass

    def __recieveMsg(self, data):
        # TODO: If connection is not established an icon should be on the tablet showing no connection symbol.
        if data == "data":
            d = data
            conn.send(bytes(d, "utf-8"))

    def handle_client(conn, addr):
        print(f"[NEW CONNECTION] {conn} Address = {addr} connected.")
        connected = True
        # TODO: When connection is made a message should be sent back to the tablet to go to the start page.
        # conn.send(bytes("connection established", "utf-8"))
        while connected:
            # now we are connected to the other flutter app.
            data = conn.recv(1024).decode()
            print(data)
        conn.close()


