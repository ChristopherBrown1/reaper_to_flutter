import reapy
from reapy import reascript_api as RPR
import socket
import threading


ADVERTISER_PORT = 3595
advertiser_conn = ''


class AdvertiserSocket:
    applicationAvailable = True

    def advertiseApplication(self):
        print("AdvertiseApplication")
        self.applicationAvailable = True
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        SERVER = s.getsockname()[0]
        s.close()
        ADDR = (SERVER, ADVERTISER_PORT)
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
        advertiser_conn.send(send_length)
        advertiser_conn.send(message)
        print(advertiser_conn.recv(64).decode(FORMAT))
        pass

    def __recieveMsg(self, data):
        # TODO: If connection is not established an icon should be on the tablet showing no connection symbol.
        if data == "data":
            d = data
            advertiser_conn.send(bytes(d, "utf-8"))

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





# TODO: Try catch to ensure that reaper is open. If not open then continue to try
HEADER = 64
PORT = 4545
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # SOCK_DGRAM is UDP, SOCK_STREAM is TCP. Try SOCK_STREAM to see if it works.
s.connect(("8.8.8.8", 80)) # Gets the ip address from the google DNS. Must have an internet connection for this to work. socket.getsockname() may also work.
SERVER = s.getsockname()[0] # Could possibly use "0.0.0.0" to bind to any ip address from this server if there are multiple addresses. Only would work for a LAN.
s.close()
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
print(f'Python Server address = {SERVER}')
conn = ''
project = reapy.Project()
advertiser = AdvertiserSocket()


def reaper_perform_id(id):
    action_id = reapy.get_command_id(id)  # converts the action id string to an int.
    reapy.perform_action(action_id)


# PUT YOUR REAPER FUNCTIONS HERE  - Use reaper_perform_id if the function needs a command id
reaper_commands = {
    "reaper hello": reapy.print,
    "play": project.play,
    "stop": project.stop,
    "rewind": reaper_perform_id,
    "mainOnCommand": reaper_perform_id,
    "send message": reapy.print,
}


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)
    print(conn.recv(64).decode(FORMAT))


def sort_data(data):
    # TODO: If connection is not established an icon should be on the tablet showing no connection symbol.
    data = data.split(':')
    try:
        if data[0] in reaper_commands:
            if len(data) == 1: # reaper commands with no parameters
                reaper_commands[data[0]]()
            elif len(data) == 2:  # reaper commands with 1 parameter
                if data[0] == "reaper hello":
                    reapy.print('Hello from flutter')
                else:
                    reaper_commands[data[0]](data[1])
            elif len(data) == 2:  # reaper commands with 2 parameters
                reaper_commands[data[0]](data[1], data[2])
    except:
        print("Error")


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {conn} Address = {addr} connected.")
    connected = True
    advertiserThread = threading.Thread(target=advertiser.stopAdvertisingApplication)
    advertiserThread.start()
    # conn.send(bytes("connection established", "utf-8"))
    while connected:
        # now we are connected to the other flutter app.
        data = conn.recv(1024).decode()
        print(data)

        if data == "exit":
            # conn.send(bytes("connection closed", "utf-8"))
            break

        sort_data(data)

    conn.close()
    advertiserThread = threading.Thread(target=advertiser.advertiseApplication)
    advertiserThread.start()


def start():
    server.listen()
    advertiserThread = threading.Thread(target=advertiser.advertiseApplication)
    advertiserThread.start()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        # Accept connections from the outside

        conn, addr = server.accept()
        print("Main socket ready")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

print("[STARTING] server is starting...")
start()
